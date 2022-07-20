from model_bakery import baker

from django.conf import settings
from django.db import IntegrityError
from django.test import TestCase

from ...recipes.models import Recipe
from ...users.models import CustomUser  # Only for type hinting
from ..models import Favourite


class FavouriteTest(TestCase):
    def setUp(self) -> None:
        self.favourite: Favourite = baker.make('favourites.Favourite')

    def test_ingredient_creation(self) -> None:
        """Проверка создания ингредиента и корректность метода __str__."""

        self.assertTrue(isinstance(self.favourite, Favourite))
        self.assertEqual(
            str(self.favourite),
            f'{self.favourite.author.full_name}: {self.favourite.recipe.name}'.strip(),
        )

    def test_author_recipe_unique_together(self) -> None:
        """Проверка совместной уникальности полей title и unit."""

        author: CustomUser = baker.make(settings.AUTH_USER_MODEL)
        recipe: Recipe = baker.make('recipes.Recipe')

        with self.assertRaises(IntegrityError):
            baker.make(
                'favourites.Favourite',
                author=author,
                recipe=recipe,
                _quantity=2,
            )
