from django.shortcuts import render

# Create your views here.

def view_purchase(request):
    """ View will render the product purchase page """
    
    return render(request, 'purchase/purchase.html')
