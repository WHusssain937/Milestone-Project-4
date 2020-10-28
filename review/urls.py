from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_reviews, name='all_reviews'),
    path('<int:review_id>/>', views.review_page, name='review_page'),
    path('add_review/', views.add_review, name='add_review'),
]
