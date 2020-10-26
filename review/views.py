from django.shortcuts import render, get_object_or_404
from .models import Review

# Create your views here.


def all_reviews(request):
    """This view will show all reviews and will include searching
     and sorting queries"""

    reviews = Review.objects.all()

    context = {
        'reviews': reviews,
    }

    return render(request, 'review/reviews.html', context)


def review_page(request, review_id):
    """This view will bring up each individual review"""

    review = get_object_or_404(Review, pk=review_id)

    context = {
        'review': review,
    }

    return render(request, 'review/review_page.html', context)
    