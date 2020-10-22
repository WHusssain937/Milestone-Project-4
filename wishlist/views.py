from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Wishlist
from profile.models import UserProfile
from cars.models import Car

# Create your views here.


def view_wishlist(request):
    """ View will render wishlist page """
    user_profile = UserProfile.objects.get(user=request.user)

    wishlist_item = Wishlist.objects.filter(user_profile=user_profile)

    context = {
        'wishlist_item': wishlist_item,
    }

    return render(request, 'wishlist/wishlist.html', context)


@login_required
def add_to_wishlist(request, car_id):
    """Adding a car to wishlist"""
    car = Car.objects.get(id=car_id)
    user_profile = UserProfile.objects.get(user=request.user)

    wished_car = Wishlist(
        car=car,
        user_profile=user_profile,
    )
    wished_car.save()

    context = {
        'wished_car': wished_car,
    }

    return redirect(reverse('view_wishlist'), context)


@login_required
def remove_wishlist_item(request, car_id):
    """ Removes a car in the wishlist """
    car = Car.objects.get(id=car_id)
    
    delete_car = Wishlist.objects.filter(car=car)
    delete_car.delete()
       
    return redirect(reverse('view_wishlist'))
