from django.shortcuts import render
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
