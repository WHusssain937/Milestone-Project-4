from django.shortcuts import render, get_object_or_404
from .models import Car

# Create your views here.


def all_cars(request):
    """ View will show all cars, including sorting and search queries """

    cars = Car.objects.all()

    context = {
        'cars': cars,
    }
    
    return render(request, 'cars/cars.html', context)

def car_detail(request, car_id):
    """ View will show details on each individual car """

    car = get_object_or_404(Car, pk=car_id)

    context = {
        'car': car,
    }
    
    return render(request, 'cars/car_details.html', context)