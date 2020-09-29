from django.shortcuts import render, get_object_or_404

from .models import Car
from .forms import Car_OrderForm


def purchase(request, car_id):
    """ View will render the product purchase page """
    car = get_object_or_404(Car, pk=car_id)

    order_form = Car_OrderForm()
    template = 'purchase/purchase.html'

    context = {
        'order_form': order_form,
        'car': car,
        'stripe_public_key': 'pk_test_51HIwyCGiwXlMOYYApouICUxrODcKuUnRPz84uzPbdBySwnVnYa4mTD3XQM16a8tI6SJalulaBlkPDtnyFxpbypPf004pZAZaIU',
        'client_secret': 'text client secret',
    }

    return render(request, template, context)
