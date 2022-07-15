from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'name',
                    'color',
                    'slug',
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
        'color',
        'slug',
    )
    search_fields = (
        'name',
        'color',
        'slug',
    )
    readonly_fields = (
        'uuid',
    )
    prepopulated_fields = {
        'slug': (
            'name',
        ),
    }
