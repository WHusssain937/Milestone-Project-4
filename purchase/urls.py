from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('<car_id>', views.purchase, name='purchase'),
    path('purchase_success/<order_number>', views.purchase_success,
         name='purchase_success'),
    path('wh/', webhook, name='webhook'),
]
