from django.shortcuts import render

# Create your views here.

def view_wishlist(request):
    """ View will return wishlist page """

    return render(request, 'wishlist/wishlist.html')