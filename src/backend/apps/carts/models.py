import uuid

from behaviors import behaviors

from django.conf import settings
from django.db import models


class Cart(behaviors.Timestamped):
    """Список покупок."""

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='cart',
        verbose_name='Владелец',
        on_delete=models.CASCADE,
    )
    recipes = models.ManyToManyField(
        'recipes.Recipe',
        related_name='carts',
        verbose_name='Рецепты',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self) -> str:
        return f'{self.owner.full_name}'
