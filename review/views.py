from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Review

# Create your views here.


def all_reviews(request):
    """This view will show all reviews and will include searching
     and sorting queries"""

    reviews = Review.objects.all()
    query = None

    if request.GET:
        if 'r' in request.GET:
            query = request.GET['r']
            if not query:
                messages.error(request, "You didn't enter any search criteria")
                return redirect(reverse('all_reviews'))

        queries = Q(make__icontains=query) | Q(model__icontains=query) | Q(year__icontains=query)

        reviews = reviews.filter(queries)

    context = {
        'reviews': reviews,
        'search_term': query,
    }

    return render(request, 'review/reviews.html', context)


def review_page(request, review_id):
    """This view will bring up each individual review"""

    review = get_object_or_404(Review, pk=review_id)

    context = {
        'review': review,
    }

    return render(request, 'review/review_page.html', context)
    