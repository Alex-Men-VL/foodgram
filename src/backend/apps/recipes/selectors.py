import typing

from django.db.models import BigAutoField
from django.db.models import QuerySet
from django.db.models.expressions import Combinable

from .models import Recipe


def get_recipes_for_current_user(
    user_id: typing.Union[
        BigAutoField[
            typing.Union[float, str, Combinable, None],
            int,
        ],
        typing.Any,
    ],
) -> 'QuerySet[Recipe]':
    """Возвращает рецепты для текущего пользователя со статусом добавления рецепта в избранное и список покупок"""

    return (
        Recipe.objects.prefetch_related(
            'tags',
            'recipe_ingredients__ingredient',
        )
        .get_with_authors_subscription_status(subscriber_id=user_id)  # type: ignore
        .get_with_favourite_status(subscriber_id=user_id)
        .get_with_is_in_shopping_cart_status(subscriber_id=user_id)
    )