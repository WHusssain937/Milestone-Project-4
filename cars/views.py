from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Car, Brand
from .forms import CarForm

# Create your views here.


def all_cars(request):
    """ View will show all cars, including sorting and search queries """

    cars = Car.objects.filter(for_sale=True)
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
            brands = request.GET['brand'].split(",")
            cars = cars.filter(brand__brand_name__in=brands)
            brands = Brand.objects.filter(brand_name__in=brands)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria")
                return redirect(reverse('cars'))

            queries = Q(make__icontains=query) | Q(model__icontains=query) \
                                               | Q(year__icontains=query) \
                                               | Q(transmission__icontains=query) \
                                               | Q(fuel_type__icontains=query)

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


@login_required
def add_car(request):
    """ Add a car to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only authorised admin can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save()
            messages.success(request, 'Successfully added car!')
            return redirect(reverse('car_detail', args=[car.id]))
        else:
            messages.error(request, 'Failed to add car. \
                                    Please ensure the form is valid.')
    else:
        form = CarForm()

    template = 'cars/add_car.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_car(request, car_id):
    """ Edit a car in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only authorised admin can do that.')
        return redirect(reverse('home'))

    car = get_object_or_404(Car, pk=car_id)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('car_detail', args=[car.id]))
        else:
            messages.error(request, 'Failed to update product. \
                                        Please ensure the form is valid.')
    else:
        form = CarForm(instance=car)
        messages.success(request, f'You are editing {car.sku}, {car.make} \
                                                {car.model} {car.year}')

    template = 'cars/edit_car.html'
    context = {
        'form': form,
        'car': car,
    }

    return render(request, template, context)


@login_required
def delete_car(request, car_id):
    """ Delete a car in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only authorised admin can do that.')
        return redirect(reverse('home'))

    car = get_object_or_404(Car, pk=car_id)
    car.delete()
    messages.success(request, 'Car has been deleted!')
    return redirect(reverse('cars'))
