import typing

from apps.users.models import CustomUser

from ..recipes.models import Recipe
from .models import Favourite


class FavouriteService:
    """Сервис для изменения избранного рецепта"""

    def __init__(self, user: typing.Union[CustomUser, typing.Any], recipe: Recipe) -> None:
        self.user: CustomUser = user
        self.recipe: Recipe = recipe

    def add_recipe_to_favorites(self) -> typing.Tuple[Favourite, bool]:
        """Добавление рецепта в избранное пользователя.

        :return: Кортеж из двух элементов: экземпляр модели `Favourite` и статус True, если рецепт добавлен в избранное,
            или False, если рецепт уже в избранном
        """

        favourite, created = Favourite.objects.get_or_create(
            user=self.user,
            recipe=self.recipe,
        )
        return favourite, created

    def remove_recipe_from_favorites(self) -> bool:
        """Удаление рецепта из списка избранных рецептов пользователя.

        :return: Результат операции: True, если рецепт удален из списка избранных рецептов, False,
            если рецепт не был в избранном
        """

        deleted, _ = Favourite.objects.filter(
            user=self.user,
            recipe=self.recipe,
        ).delete()
        return deleted
