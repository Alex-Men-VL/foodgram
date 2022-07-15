from django.contrib import admin

from .models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'title',
                    'unit',
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
        'title',
        'unit',
    )
    search_fields = (
        'title',
        'unit',
    )
    readonly_fields = (
        'uuid',
    )
