from django.shortcuts import render, redirect, reverse, get_object_or_404
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

    return redirect(reverse('view_wishlist'), context)
    