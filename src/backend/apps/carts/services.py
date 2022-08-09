import typing

from apps.users.models import CustomUser

from ..recipes.models import Recipe
from .models import Cart


class CartService:
    """Сервис для изменения списка покупок пользователя"""

    def __init__(self, user: typing.Union[CustomUser, typing.Any], recipe: Recipe) -> None:
        self.user: CustomUser = user
        self.recipe: Recipe = recipe

    def add_recipe_to_shopping_cart(self) -> typing.Tuple[Cart, bool]:
        """Добавление рецепта в список покупок пользователя.

        :return: Кортеж из двух элементов: экземпляр модели `Cart` и статус True, если рецепт добавлен в список покупок,
            или False, если рецепт уже в списке покупок
        """

        user_cart = self._get_or_create_user_cart()

        if self.recipe.pk in user_cart.recipes.values_list('id', flat=True):
            return user_cart, False

        user_cart.recipes.add(self.recipe)
        return user_cart, True

    def remove_recipe_from_shopping_cart(self) -> bool:
        """Удаление рецепта из списка покупок пользователя.

        :return: Результат операции: True, если рецепт удален из списка покупок пользователя, False,
            если рецепт не был в списке покупок
        """

        user_cart = self._get_or_create_user_cart()

        if self.recipe.pk not in user_cart.recipes.values_list('id', flat=True):
            return False

        user_cart.recipes.remove(self.recipe)
        return True

    def _get_or_create_user_cart(self) -> Cart:
        """Возвращает список покупок пользователя"""

        if hasattr(self, 'user_cart'):  # pragma: no cover
            return self.user_cart  # type: ignore

        user_cart, _ = (
            Cart.objects
            .prefetch_related(
                'recipes',
            )
            .get_or_create(
                owner=self.user,
            )
        )

        self.user_cart = user_cart
        return user_cart
