from django.contrib import admin

from .models import Wishlist


class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        'user_profile',
        'car',
    )

    ordering = ('user_profile',)


admin.site.register(Wishlist, WishlistAdmin)
