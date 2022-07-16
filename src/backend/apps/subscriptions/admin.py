from django.contrib import admin

from .models import Subscription


class SubscriptionInline(admin.TabularInline):
    model = Subscription
    fk_name = 'subscriber'
    extra = 2
    classes = (
        'collapse',
    )
    fields = (
        'author',
    )
    raw_id_fields = (
        'author',
    )
    verbose_name = 'Подписка на автора'
    verbose_name_plural = 'Подписки на авторов'
