import typing

from django.db.models import BigAutoField
from django.db.models import QuerySet
from django.db.models.expressions import Combinable

from apps.tags.models import Tag

from .models import Recipe
from .models import RecipeIngredient


def get_recipes_for_current_user(
    user_id: typing.Union[
        BigAutoField[
            typing.Union[float, str, Combinable, None],
            int,
        ],
        typing.Any,
    ],
    recipe_id: typing.Union[
        BigAutoField[
            typing.Union[float, str, Combinable, None],
            int,
        ],
        typing.Any,
    ] = None,
) -> 'QuerySet[Recipe]':
    """Возвращает рецепты для текущего пользователя со статусом добавления рецепта в избранное и список покупок

    :param user_id: Id пользователя
    :param recipe_id: Id рецепта

    :return Если передан `recipe_id`, возвращается указанный рецепт, либо None
    """

    recipes = (
        Recipe.objects.prefetch_related(
            'tags',
            'recipe_ingredients__ingredient',
        )
        .get_with_authors_subscription_status(subscriber_id=user_id)  # type: ignore
        .get_with_favourite_status(subscriber_id=user_id)
        .get_with_is_in_shopping_cart_status(subscriber_id=user_id)
    )

    if recipe_id:
        return recipes.filter(pk=recipe_id).first()
    return recipes


def get_recipe_ingredients(
    recipe: Recipe,
) -> 'QuerySet[RecipeIngredient]':
    """Возвращает список ингредиентов рецепта

    :param recipe: Рецепт
    """

    return RecipeIngredient.objects.filter(
        recipe=recipe,
    )


def get_author_recipes_for_current_user(
    author_id: typing.Union[
        BigAutoField[
            typing.Union[float, str, Combinable, None],
            int,
        ],
        typing.Any,
    ],
    user_id: typing.Union[
        BigAutoField[
            typing.Union[float, str, Combinable, None],
            int,
        ],
        typing.Any,
    ],
) -> 'QuerySet[Recipe]':
    """Возвращает рецепты указанного автора для текущего пользователя

    :param author_id: Id автора
    :param user_id: Id текущего пользователя
    """

    recipes = get_recipes_for_current_user(user_id)
    return recipes.filter(author_id=author_id)


def get_recipes_for_current_user_by_tags(
    user_id: typing.Union[
        BigAutoField[
            typing.Union[float, str, Combinable, None],
            int,
        ],
        typing.Any,
    ],
    tags: typing.Sequence['Tag'],
) -> 'QuerySet[Recipe]':
    """Возвращает рецепты для текущего пользователя, отфильтрованные по слагам переданных тегов

    :param user_id: Id текущего пользователя
    :param tags: Список тегов
    """

    recipes = get_recipes_for_current_user(user_id)

    for tag in tags:
        recipes = recipes.filter(tags__slug=tag.slug)

    return recipes
