from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Car, Brand

# Create your views here.


def all_cars(request):
    """ View will show all cars, including sorting and search queries """

    cars = Car.objects.all()
    query = None
    brand = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'brand':
                sortkey = 'brand__brand_name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            cars = cars.order_by(sortkey)

        if 'brand' in request.GET:
            print('#######################################')
            brands = request.GET['brand'].split(",")
            print(brands)
            cars = cars.filter(brand__brand_name__in=brands)
            print(cars)
            brands = Brand.objects.filter(brand_name__in=brands)
            
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria")
                return redirect(reverse('cars'))
    
            queries = Q(make__icontains=query) | Q(model__icontains=query)
            cars = cars.filter(queries)   
    
    current_sorting = f'{sort}_{direction}'

    context = {
        'cars': cars,
        'search_term': query,
        'current_brands': brand,
        'current_sorting': current_sorting,
    }

    return render(request, 'cars/cars.html', context)


def car_detail(request, car_id):
    """ View will show details on each individual car """

    car = get_object_or_404(Car, pk=car_id)

    context = {
        'car': car,
    }
    
    return render(request, 'cars/car_details.html', context)