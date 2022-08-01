from django.test import TestCase

from apps.favourites.models import Favourite
from apps.recipes.models import Recipe
from apps.users.models import CustomUser

from ..factories import FavouriteFactory
from ..factories import RecipeFactory
from ..factories import UserFactory


class FavouriteTest(TestCase):
    def setUp(self) -> None:
        self.user: CustomUser = UserFactory()
        self.recipe: Recipe = RecipeFactory(author=self.user)
        self.favourite: Favourite = FavouriteFactory(author=self.user, recipe=self.recipe)

    def test_favourite_creation(self) -> None:
        """Проверка добавления ингредиента в избранное и корректность метода __str__."""

        self.assertEqual(self.favourite.author, self.user)
        self.assertEqual(self.favourite.recipe, self.recipe)

        self.assertTrue(isinstance(self.favourite, Favourite))
        self.assertEqual(
            str(self.favourite),
            f'{self.favourite.author.full_name}: {self.favourite.recipe.name}'.strip(),
        )
