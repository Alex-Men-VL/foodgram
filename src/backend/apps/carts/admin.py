from django.contrib import admin

from .models import Cart


class RecipeInline(admin.TabularInline):
    model = Cart.recipes.through
    extra = 2
    fields = ('recipe',)
    raw_id_fields = ('recipe',)
    verbose_name = 'Рецепт'
    verbose_name_plural = 'Покупки test'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                'fields': ('owner',),
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
    list_display = ('owner',)
    search_fields = ('owner',)
    inlines = (RecipeInline,)
    readonly_fields = ('uuid',)
    raw_id_fields = ('owner',)
