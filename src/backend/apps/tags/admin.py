from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'title',
                    'hex_code',
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
        'title',
        'hex_code',
        'slug',
    )
    search_fields = (
        'title',
        'hex_code',
        'slug',
    )
    readonly_fields = (
        'uuid',
    )
    prepopulated_fields = {
        'slug': (
            'title',
        ),
    }
