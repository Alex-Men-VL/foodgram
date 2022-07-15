import uuid

from behaviors import behaviors

from django.db import models


class Ingredient(behaviors.Timestamped):
    """Ингредиенты для рецептов."""

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    name = models.CharField(
        'Название',
        max_length=255,
        db_index=True,
    )
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=100,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = (
            'name',
        )
        unique_together = (
            'name',
            'measurement_unit',
        )

    def __str__(self) -> str:
        return f'{self.name}, {self.measurement_unit}'.strip()
