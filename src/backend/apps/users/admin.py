from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import forms
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
                'fields': (
                    'is_staff',
                    'is_active',
                    'groups',
                ),
            },
        ),
        (
            'Техническая информация',
            {
                'classes': (
                    'collapse',
                ),
                'fields': (
                    'uuid',
                ),
            },
        ),
    )
    readonly_fields = (
        'uuid',
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': (
                    'wide',
                ),
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
