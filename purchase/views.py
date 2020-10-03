from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .models import Car_Order
from cars.models import Car
from .forms import Car_OrderForm

import stripe


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
            car = Car.objects.get(id=car_id)
            order.car = car
            order.user = request.user
            order.save()
        
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
           amount=car.price,
           currency=settings.STRIPE_CURRENCY,
        )

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

    return render(request, template, context)


def purchase_success(request, order_number):
    """
    Handle Successful Purchases
    """
    save_info = request.session.get('save-info')
    car_order = get_object_or_404(Car_Order, order_number=order_number)
    messages.success(request, f'Your Order Has Been Processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {car_order.email}.')

    template = 'purchase/purchase_success.html'
    context = {
        'car_order': car_order,
    }

    return render(request, template, context)
