import uuid

from behaviors import behaviors

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.db.models import QuerySet

CustomUser = get_user_model()


class RecipeQuerySet(QuerySet):
    def get_with_authors_subscription_status(
        self,
        subscriber_id: int,
    ) -> 'QuerySet':
        """Возвращает рецепты со статусом подписки на автора"""

        authors_prefetch = models.Prefetch(
            'author',
            CustomUser.objects.get_with_subscription_status(subscriber_id),
        )
        return self.prefetch_related(authors_prefetch)


class Recipe(behaviors.Timestamped):
    """Рецепты."""

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    name = models.CharField(
        'Название',
        max_length=255,
        db_index=True,
        unique=True,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='recipes',
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/images',
    )
    text = models.TextField(
        'Текстовое описание',
    )
    ingredients = models.ManyToManyField(
        'ingredients.Ingredient',
        related_name='recipes',
        verbose_name='Ингредиенты',
        through='RecipeIngredient',
    )
    tags = models.ManyToManyField(
        'tags.Tag',
        related_name='recipes',
        verbose_name='Теги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[
            validators.MinValueValidator(1),
        ],
        help_text='В минутах.',
    )

    objects = RecipeQuerySet.as_manager()

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = [
            'name',
        ]

    def __str__(self) -> str:
        return f'{self.name}'.strip()


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        'ingredients.Ingredient',
        related_name='recipe_ingredients',
        verbose_name='Ингредиент',
        on_delete=models.PROTECT,
        db_index=True,
    )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        related_name='recipe_ingredients',
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        db_index=True,
    )
    amount = models.PositiveIntegerField(
        'Количество',
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        unique_together = (
            'ingredient',
            'recipe',
        )

    def __str__(self) -> str:
        return f'{self.recipe}: {self.ingredient.name} {self.amount}'.strip()
