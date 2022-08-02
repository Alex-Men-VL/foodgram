import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.db import models
from django.db.models.query import QuerySet

from ..subscriptions.models import Subscription


class CustomUserQuerySet(models.QuerySet):
    def get_with_recipes(self) -> 'QuerySet[CustomUser]':
        """Возвращает пользователей вместе с рецептами"""

        return self.prefetch_related(
            'recipes',
        )

    def get_with_recipes_count(self) -> 'QuerySet[CustomUser]':
        """Возвращает пользователей вместе с количеством их рецептов"""

        return self.annotate(
            recipes_count=models.Count('recipes'),
        )

    def get_with_subscription_status(
        self,
        subscriber_id: int,
    ) -> 'QuerySet[CustomUser]':
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
    ) -> 'QuerySet[CustomUser]':
        """Возвращает пользователей вместе со статусом подписки текущего пользователя, переданным в аргументе

        :param is_subscribed: Статус подписки
        """

        return self.annotate(
            is_subscribed=models.Value(
                is_subscribed,
                output_field=models.BooleanField(),
            ),
        )


class CustomUserManager(UserManager.from_queryset(CustomUserQuerySet)):
    use_in_migrations = True


class CustomUser(AbstractUser):
    uuid = models.UUIDField(
        db_index=True,
        unique=True,
        default=uuid.uuid4,
    )

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'.strip()

    def __str__(self) -> str:
        return self.full_name
