from django.test import TestCase

from apps.ingredients.models import Ingredient
from apps.recipes.models import Recipe
from apps.recipes.models import RecipeIngredient
from apps.users.models import CustomUser

from ...factories import IngredientFactory
from ...factories import RecipeFactory
from ...factories import RecipeIngredientFactory
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


class RecipeIngredientTest(TestCase):
    def setUp(self) -> None:
        self.recipe: Recipe = RecipeFactory()
        self.ingredient: Ingredient = IngredientFactory()
        self.recipe_ingredient: RecipeIngredient = RecipeIngredientFactory(
            recipe=self.recipe,
            ingredient=self.ingredient,
        )

    def test_recipe_ingredient_creation(self) -> None:
        """Проверка создания ингредиента для рецепта и корректность метода __str__."""

        self.assertTrue(isinstance(self.recipe_ingredient, RecipeIngredient))
        self.assertEqual(
            str(self.recipe_ingredient),
            f'{self.recipe}: {self.ingredient.name} {self.recipe_ingredient.amount}'.strip(),
        )
