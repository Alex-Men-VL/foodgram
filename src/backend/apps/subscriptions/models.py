import uuid

from behaviors import behaviors

from django.conf import settings
from django.core.exceptions import ValidationError
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
        unique_together = (
            'subscriber',
            'author',
        )
        ordering = (
            'created',
        )

    def __str__(self) -> str:
        return f'{self.subscriber.full_name}: {self.author.full_name}'

    def clean(self) -> None:
        # Не позволять подписаться на самого себя
        if self.author == self.subscriber:
            raise ValidationError('Нельзя подписываться на самого себя.')
