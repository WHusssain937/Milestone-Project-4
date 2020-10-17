from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm

from purchase.models import Car_Order


def profile(request):
    """ Display's the user's profile """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update Failed. Please ensure form is valid.')    
    else:
        form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profile/profile.html'
    context = {
        'form': form,
        'orders': orders,
    }

    return render(request, template, context)


def order_history(request, order_number):
    car_order = get_object_or_404(Car_Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'purchase/purchase_success.html'
    context = {
        'car_order': car_order,
        'from_profile': True,
    }

    return render(request, template, context)
