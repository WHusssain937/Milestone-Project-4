from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .models import Car
from .forms import Car_OrderForm

import stripe


def purchase(request, car_id):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

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
