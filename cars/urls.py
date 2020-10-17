from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_cars, name='cars'),
    path('<int:car_id>/>', views.car_detail, name='car_detail'),
    path('add/', views.add_car, name='add_car'),
    path('edit/<int:car_id>/', views.edit_car, name='edit_car'),
    path('delete/<int:car_id>/', views.delete_car, name='delete_car'),
]