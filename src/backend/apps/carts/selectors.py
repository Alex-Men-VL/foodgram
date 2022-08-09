import typing

from django.db import models
from django.db.models.expressions import Combinable

from ..recipes.models import Recipe
from ..recipes.models import RecipeIngredient
from .models import Cart


def get_user_cart(
    user_id: typing.Union[
        models.BigAutoField[
            typing.Union[float, str, Combinable, None],
            int,
        ],
        typing.Any,
    ],
) -> typing.Union[Cart, None]:
    """Возвращает список покупок пользователя

    :param user_id: Id пользователя

    :return: Список покупок пользователя, либо None, если его нет
    """

    user_cart = Cart.objects.filter(owner_id=user_id).first()
    return user_cart


def get_cart_recipe(
    user_id: typing.Union[
        models.BigAutoField[
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

    user_cart = get_user_cart(user_id)

    if not user_cart:
        return None

    cart_recipe = user_cart.recipes.filter(pk=recipe_id).first()
    return cart_recipe


def check_cart_contains_recipes(
    cart: Cart,
) -> bool:
    """Проверка наличия рецептов в списке покупок

    :param cart: Список покупок

    :return: True, если в списке покупок есть рецепты, иначе - False
    """

    return cart.recipes.exists()


def get_cart_recipes(
    cart: Cart,
) -> 'models.QuerySet[Recipe]':
    """Получение рецептов из списка покупок

    :param cart: Список покупок
    """

    return cart.recipes.values('pk')


def get_cart_total_ingredients_amount(
    cart_recipes: 'models.QuerySet[Recipe]',
) -> typing.List[typing.Dict[str, typing.Union[str | int]]]:
    """Получение списка ингредиентов из списка покупок с общим количеством

    :param cart_recipes: Рецепты из списка покупок
    """

    cart_ingredients = (
        RecipeIngredient.objects.filter(
            recipe__in=cart_recipes,
        )
        .select_related(
            'ingredient',
        )
        .values(
            ingredient_name=models.F('ingredient__name'),
            ingredient_measurement_unit=models.F('ingredient__measurement_unit'),
        ).annotate(
            amount=models.Sum('amount'),
        )
    )

    return list(cart_ingredients)
