from django.contrib.auth.models import UserManager
from django.db import models
from django.db.models import QuerySet

from ..subscriptions.models import Subscription


class CustomUserQuerySet(models.QuerySet):
    def get_with_recipes(self) -> 'QuerySet':
        """Возвращает пользователей вместе с рецептами"""

        return self.prefetch_related(
            'recipes',
        )

    def get_with_recipes_count(self) -> 'QuerySet':
        """Возвращает пользователей вместе с количеством их рецептов"""

        return self.annotate(
            recipes_count=models.Count('recipes'),
        )

    def get_with_subscription_status(
        self,
        subscriber_id: int,
    ) -> 'QuerySet':
        """Возвращает пользователей вместе со статусом, является ли переданный пользователь его подписчиком

        :param subscriber_id: id проверяемого пользователя
        """

        subscribers = Subscription.objects.filter(
            author=models.OuterRef('pk'),
        )
        return self.annotate(
            is_subscribed=models.Exists(
                subscribers.filter(
                    subscriber_id=subscriber_id,
                ),
            ),
        )

    def set_default_subscription_status(
        self,
        is_subscribed: bool,
    ) -> 'QuerySet':
        """Возвращает пользователей вместе со статусом подписки текущего пользователя, переданным в аргументе

        :param is_subscribed: Статус подписки
        """

        return self.annotate(
            is_subscribed=models.Value(
                is_subscribed,
                output_field=models.BooleanField(),
            ),
        )


class CustomUserManager(UserManager.from_queryset(CustomUserQuerySet)):  # type: ignore
    use_in_migrations = True
