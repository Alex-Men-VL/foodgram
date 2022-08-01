from django.test import TestCase

from apps.recipes.models import Recipe
from apps.users.models import CustomUser

from ...factories import RecipeFactory
from ...factories import UserFactory


class RecipeTest(TestCase):
    def setUp(self) -> None:
        self.user: CustomUser = UserFactory()
        self.recipe: Recipe = RecipeFactory(author=self.user)

    def test_recipe_creation(self) -> None:
        """Проверка создания ингредиента и корректность метода __str__."""

        self.assertEqual(self.recipe.author, self.user)

        self.assertTrue(isinstance(self.recipe, Recipe))
        self.assertEqual(str(self.recipe), f'{self.recipe.name}'.strip())
