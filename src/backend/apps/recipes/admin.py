from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import SafeString

from .models import Recipe


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 2
    classes = ('collapse',)
    fields = (
        'amount',
        'ingredient',
    )
    raw_id_fields = ('ingredient',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'name',
                    'image',
                    'author',
                    'text',
                    'tags',
                    'cooking_time',
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
        'author',
        'get_image_preview',
    )
    search_fields = ('name',)
    list_filter = (
        'author',
        'tags',
    )
    inlines = (RecipeIngredientInline,)
    readonly_fields = ('uuid',)
    raw_id_fields = ('tags',)

    @admin.display(description='Изображение')
    def get_image_preview(self, obj: Recipe) -> SafeString:
        return format_html(
            '<img src="{url}" style="max-height: 200px;"/>',
            url=obj.image.url,
        )
