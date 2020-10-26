from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_reviews, name='all_reviews'),
    path('<review_id>', views.review_page, name='review_page'),
]