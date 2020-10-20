import uuid

from django.db import models
from django.conf import settings

from django_countries.fields import CountryField

from cars.models import Car
from profile.models import UserProfile


class Car_Order(models.Model):

    car = models.ForeignKey(Car, null=False, blank=False, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, 
                                     null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.CharField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date_of_purchase = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=6, decimal_places=0, null=False, default=0)
    original_purchase = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        """
        Generates a ramdom order number using UUID
        """
        return uuid.uuid4().hex.upper()
    
    def save(self, *args, **kwargs):
        """
        Overrides the orginal save method to set the orginal
        order number if it has been set already 
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number
