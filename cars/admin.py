from django.contrib import admin
from .models import Car, Brand

# Register your models here.


class CarAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'brand',
        'make',
        'model',
        'year',
        'price',
        'image'
    )

    ordering = ('brand',)


class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'brand_name',
    )


admin.site.register(Car, CarAdmin)
admin.site.register(Brand, BrandAdmin)
