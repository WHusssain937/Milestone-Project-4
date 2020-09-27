from django.urls import path
from . import views

urlpatterns = [
    path('<car_id>', views.purchase, name='purchase'),
]
