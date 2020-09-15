from django.shortcuts import render
from .models import Car

# Create your views here.


def all_cars(request):
    """ View will return all cars, including sorting and search queries """

    cars = Car.objects.all()

    context = {
        'cars': cars,
    }
    
    return render(request, 'cars/cars.html', context)