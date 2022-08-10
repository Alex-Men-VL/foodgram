import uuid

from behaviors import behaviors

from django.conf import settings
from django.db import models


class Subscription(behaviors.Timestamped):
    """Подписка на автора."""

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='subscriptions',
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        help_text='Тот, кто подписался.',
        db_index=True,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='subscribers',
        verbose_name='Автор',
        on_delete=models.CASCADE,
        help_text='Тот, на кого подписался.',
        db_index=True,
    )

    class Meta:
        verbose_name = 'Подписка на автора'
        verbose_name_plural = 'Подписки на авторов'
        ordering = ('created',)
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'subscriber',
                    'author',
                ),
                name='%(app_label)s_%(class)s_subscriber_author_unique_together',
            ),
            models.CheckConstraint(
                check=~models.Q(subscriber=models.F('author')),
                name='%(app_label)s_%(class)s_prevent_self_follow',
            ),
        )

    def __str__(self) -> str:
        return f'{self.subscriber.full_name}: {self.author.full_name}'
