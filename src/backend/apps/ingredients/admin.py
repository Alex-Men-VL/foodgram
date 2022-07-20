from django.contrib import admin

from .models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'name',
                    'measurement_unit',
                ),
            },
        ),
        (
            'Техническая информация',
            {
                'classes': ('collapse',),
                'fields': ('uuid',),
            },
        ),
    )
    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = (
        'name',
        'measurement_unit',
    )
    readonly_fields = ('uuid',)
