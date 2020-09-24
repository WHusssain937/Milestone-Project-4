from django.shortcuts import render

from .forms import Car_OrderForm


def purchase(request):
    """ View will render the product purchase page """
    order_form = Car_OrderForm()
    template = 'purchase/purchase.html'
    
    context = {
        'order_form': order_form,
    }

    return render(request, template, context)
