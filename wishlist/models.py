from django.db import models

from cars.models import Car
from profile.models import UserProfile


class Wishlist(models.Model):
    car = models.ForeignKey(Car, null=False, blank=False,
                            on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True)

    def __str__(self):
        return self.car.make
