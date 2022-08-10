import uuid

from behaviors import behaviors
from slugify import slugify

from django.db import models
from django.db.models import functions

models.CharField.register_lookup(functions.Length, 'len')


class Tag(behaviors.Slugged, behaviors.Timestamped):
    """Теги для рецептов."""

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    name = models.CharField(
        'Название',
        max_length=255,
        unique=True,
    )
    color = models.CharField(
        'Цветовой HEX-код',
        max_length=7,
        unique=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'name',
                    'color',
                ),
                name='%(app_label)s_%(class)s_name_color_unique_together',
            ),
            models.CheckConstraint(
                check=models.Q(name__len__gt=0),
                name='%(app_label)s_%(class)s_name_is_empty',
            ),
            models.CheckConstraint(
                check=(
                    models.Q(color__startswith='#')
                    & models.Q(color__len__in=(4, 7))
                ),
                name='%(app_label)s_%(class)s_color_is_not_hex_code',
            ),
        )

    @property
    def slug_source(self) -> str:
        return slugify(self.name)

    def __str__(self) -> str:
        return f'{self.name}'.strip()
