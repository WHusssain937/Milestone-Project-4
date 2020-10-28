from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_reviews, name='all_reviews'),
    path('<int:review_id>/>', views.review_page, name='review_page'),
    path('add_review/', views.add_review, name='add_review'),
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
]
