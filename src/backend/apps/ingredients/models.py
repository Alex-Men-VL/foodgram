import uuid

from behaviors import behaviors

from django.db import models
from django.db.models import functions

models.CharField.register_lookup(functions.Length, 'len')


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
        ordering = ('name',)
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'name',
                    'measurement_unit',
                ),
                name='%(app_label)s_%(class)s_name_measurement_unit_unique_together',
            ),
            models.CheckConstraint(
                check=models.Q(name__len__gt=0),
                name='%(app_label)s_%(class)s_name_is_empty',
            ),
            models.CheckConstraint(
                check=models.Q(measurement_unit__len__gt=0),
                name='%(app_label)s_%(class)s_measurement_unit_is_empty',
            ),
        )

    def __str__(self) -> str:
        return f'{self.name}, {self.measurement_unit}'.strip()
