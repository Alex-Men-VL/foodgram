import uuid

from behaviors import behaviors
from slugify import slugify

from django.db import models

from .validators import validate_title_is_hexa_code


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
        validators=[
            validate_title_is_hexa_code,
        ],
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        unique_together = (
            'name',
            'color',
        )

    @property
    def slug_source(self) -> str:
        return slugify(self.name)

    def __str__(self) -> str:
        return f'{self.name}'.strip()
