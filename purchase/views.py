from django.shortcuts import render, reverse, redirect, get_object_or_404, \
                             HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import Car_Order
from cars.models import Car
from profile.forms import UserProfileForm
from profile.models import UserProfile
from .forms import Car_OrderForm

import stripe


@require_POST
def cache_purchase_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'car_id': request.session.get('car_id'),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


@login_required
def purchase(request, car_id):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        car_id = request.POST['car_id']

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = Car_OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = str(pid)
            order.original_purchase = car_id
            car = Car.objects.get(id=car_id)
            order.car = car
            order.total = car.price
            order.save()

            car.for_sale = False
            car.save()
            
            request.session['save_info'] = 'save-info' in request.POST

            return redirect(reverse('purchase_success',
                            args=[order.order_number]))

        else:
            messages.error(request, 'Error with Form, \
                Please Check and Try Again.')
    else:
        car = get_object_or_404(Car, pk=car_id)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
           amount=int(car.price*100),
           currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = Car_OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = Car_OrderForm()
        else:
            order_form = Car_OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'purchase/purchase.html'
    context = {
        'order_form': order_form,
        'car': car,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    request.session['car_id'] = car_id
    return render(request, template, context)


def purchase_success(request, order_number):
    """
    Handle Successful Purchases
    """
    save_info = request.session.get('save_info')
    car_order = get_object_or_404(Car_Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        car_order.user_profile = profile
        car_order.save()

    if save_info:
        profile_data = {
            'default_phone_number': car_order.phone_number,
            'default_country': car_order.country,
            'default_postcode': car_order.postcode,
            'default_town_or_city': car_order.town_or_city,
            'default_street_address1': car_order.street_address1,
            'default_street_address2': car_order.street_address2,
            'default_county': car_order.county,
        }
        user_profile_form = UserProfileForm(profile_data, instance=profile)
        if user_profile_form.is_valid():
            user_profile_form.save()

    messages.success(request, f'Your Order Has Been Processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {car_order.email}.')

    template = 'purchase/purchase_success.html'
    context = {
        'car_order': car_order,
    }

    return render(request, template, context)
