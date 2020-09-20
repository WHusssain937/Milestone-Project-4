from django.urls import path
from . import views

urlpatterns = [
    path('purchase/', views.view_purchase, name='purchase'),
]