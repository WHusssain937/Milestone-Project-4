from django.db import models


class Brand(models.Model):
    brand_name = models.CharField(max_length=254)
    
    def __str__(self):
        return self.brand_name


class Car(models.Model):
    brand = models.ForeignKey('Brand', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    make = models.CharField(max_length=254)
    model = models.CharField(max_length=254)
    year = models.IntegerField(null=True, blank=True)
    mileage = models.CharField(max_length=254, null=True, blank=True)
    fuel_type = models.CharField(max_length=254, null=True, blank=True)
    transmission = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=0)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.make
