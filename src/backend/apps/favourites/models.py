import uuid

from behaviors import behaviors

from django.conf import settings
from django.db import models


class Favourite(behaviors.Timestamped):
    """Избранное."""

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        related_name='favourites',
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        db_index=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='favourites',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'recipe',
                    'user',
                ),
                name='%(app_label)s_%(class)s_recipe_user_unique_together',
            ),
        )

    def __str__(self) -> str:
        return f'{self.user.full_name}: {self.recipe.name}'.strip()
