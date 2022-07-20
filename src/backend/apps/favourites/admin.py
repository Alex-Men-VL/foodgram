from django.contrib import admin

from .models import Favourite


class FavouriteInline(admin.TabularInline):
    model = Favourite
    extra = 2
    classes = ('collapse',)
    fields = ('recipe',)
    raw_id_fields = ('recipe',)
    verbose_name = 'Избранное'
    verbose_name_plural = 'Избранное'
