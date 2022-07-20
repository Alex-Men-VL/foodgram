from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html

from . import forms
from ..carts.models import Cart
from ..favourites.admin import FavouriteInline
from ..subscriptions.admin import SubscriptionInline
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = forms.CustomUserCreationForm
    form = forms.CustomUserChangeForm
    list_display = (
        'username',
        'first_name',
        'last_name',
        'is_staff',
        'email',
    )
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'username',
                ),
            },
        ),
        (
            'Права',
            {
                'classes': ('collapse',),
                'fields': (
                    'is_staff',
                    'is_active',
                    'groups',
                ),
            },
        ),
        (
            'Список покупок',
            {
                'classes': ('collapse',),
                'fields': ('get_user_cart',),
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
    readonly_fields = (
        'uuid',
        'get_user_cart',
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'first_name',
                    'last_name',
                    'username',
                    'email',
                    'password1',
                    'password2',
                    'is_staff',
                    'is_active',
                    'groups',
                ),
            },
        ),
    )
    inlines = (
        FavouriteInline,
        SubscriptionInline,
    )

    @admin.display(description='Список покупок')
    def get_user_cart(self, obj: CustomUser) -> str:
        try:
            cart: Cart = obj.cart
        except Cart.DoesNotExist:
            url: str = '{}?{}'.format(
                reverse('admin:carts_cart_add'),
                f'owner={obj.pk}',
            )
            message: str = 'Добавить.'
        else:
            url = '{}'.format(
                reverse(
                    'admin:carts_cart_change',
                    args=(cart.pk,),
                ),
            )
            message = 'Просмотреть.'

        return format_html(
            '<a href="{}">{}</a>',
            url,
            message,
        )
