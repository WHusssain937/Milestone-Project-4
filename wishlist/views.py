from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Wishlist
from profile.models import UserProfile
from cars.models import Car


@login_required
def view_wishlist(request):
    """ View will render wishlist page """

    user_profile = UserProfile.objects.get(user=request.user)

    wishlist_item = Wishlist.objects.filter(user_profile=user_profile,
                                            car__for_sale=True)

    context = {
        'wishlist_item': wishlist_item,
    }

    return render(request, 'wishlist/wishlist.html', context)


@login_required
def add_to_wishlist(request, car_id):
    """Adding a car to wishlist"""
    car = Car.objects.get(id=car_id)
    user_profile = UserProfile.objects.get(user=request.user)

    wished_car, created = Wishlist.objects.get_or_create(
        car=car,
        user_profile=user_profile,
    )
    wished_car.save()

    if created:
        # When car is added to wishlist
        messages.success(request, f'{car.make} {car.model} {car.year} \
                         has been successfully added to your Wishlist')
    else:
        # when car has already been added to wishlist
        messages.info(request, f'{car.sku}, {car.make} {car.model} {car.year} \
                      is already in your wishlist')
        return redirect(reverse('car_detail', args=[car.id]))

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

    messages.success(request, f'You have removed {car.sku}, {car.make} \
                     {car.model} {car.year} successfully from the Wishlist.')

    return redirect(reverse('view_wishlist'))
