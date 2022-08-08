import typing

from django.db.models import BigAutoField
from django.db.models.expressions import Combinable

from apps.recipes.models import Recipe

from .models import Cart


def get_cart_recipe(
    user_id: typing.Union[
        BigAutoField[
            typing.Union[float, str, Combinable, None],
            int,
        ],
        typing.Any,
    ],
    recipe_id: typing.Union[str, int],
) -> typing.Union[Recipe, None]:
    """Возвращает рецепт из списка покупок пользователя

    :param user_id: Id пользователя
    :param recipe_id: Id рецепта
    """

    user_cart = Cart.objects.filter(owner_id=user_id).first()

    if not user_cart:
        return None

    cart_recipe: Recipe = user_cart.recipes.filter(pk=recipe_id).first()
    return cart_recipe
