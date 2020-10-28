from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Review
from cars.models import Brand
from .forms import ReviewForm

# Create your views here.


def all_reviews(request):
    """This view will show all reviews and will include searching
     and sorting queries"""

    reviews = Review.objects.all()
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
            reviews = reviews.order_by(sortkey)

        if 'brand' in request.GET:
            brands = request.GET['brand'].split(",")
            reviews = reviews.filter(brand__brand_name__in=brands)
            brands = Brand.objects.filter(brand_name__in=brands)
        
        if 'r' in request.GET:
            query = request.GET['r']
            if not query:
                messages.error(request, "You didn't enter any Search Criteria")
                return redirect(reverse('all_reviews'))

            queries = Q(make__icontains=query) | Q(model__icontains=query) | Q(year__icontains=query)

            reviews = reviews.filter(queries)
    
    current_sorting = f'{sort}_{direction}'
        
    context = {
        'reviews': reviews,
        'search_term': query,
        'current_brands': brand,
        'current_sorting': current_sorting,
    }

    return render(request, 'review/reviews.html', context)


def review_page(request, review_id):
    """This view will bring up each individual review"""

    review = get_object_or_404(Review, pk=review_id)

    context = {
        'review': review,
    }

    return render(request, 'review/review_page.html', context)


# @login_required
def add_review(request):
    """ Add a car to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only authorised admin can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save()
            messages.success(request, 'Successfully added car!')
            return redirect(reverse('review_page', args=[review.id]))
        else:
            messages.error(request, 'Failed to add car. Please ensure the form is valid.')
    else:
        form = ReviewForm()

    template = 'review/add_review.html'
    context = {
        'form': form,
    }

    return render(request, template, context)