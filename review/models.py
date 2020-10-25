from django.db import models

from cars.models import Brand


class Review(models.Model):
    brand = models.ForeignKey(Brand, null=False, blank=False, 
                              on_delete=models.CASCADE)
    make = models.CharField(max_length=254)
    model = models.CharField(max_length=254)
    year = models.IntegerField(null=True, blank=True)
    advantage = models.CharField(max_length=254, null=True, blank=True)
    disadvantage = models.CharField(max_length=254, null=True, blank=True)
    review_by = models.CharField(max_length=254)
    car_review = models.TextField()
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return '{}, {}, {}'.format(self.make, self.model, self.year)
