from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Wishlist
from profile.models import UserProfile
from cars.models import Car

# Create your views here.


def view_wishlist(request):
    """ View will return wishlist page """

    return render(request, 'wishlist/wishlist.html')


@login_required
def add_to_wishlist(request, car_id):
    """Adding a car to wishlist"""
    car = get_object_or_404(Car, pk=car_id)
    user_profile = UserProfile.objects.get(user=request.user)

    wished_car = Wishlist(
        car=car,
        user_profile=user_profile,
    )
    wished_car.save()

    context = {
        'car': car,
        'user_profile': user_profile,
    }

    return render(request, 'wishlist/wishlist.html', context)
    