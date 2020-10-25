from django.contrib import admin

from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'brand',
        'make',
        'model',
        'year',
        'review_by',
        'image'
    )

    ordering = ('brand',)


admin.site.register(Review, ReviewAdmin)
