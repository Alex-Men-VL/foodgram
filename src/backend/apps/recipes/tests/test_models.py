from model_bakery import baker

from django.test import TestCase

from ..models import Recipe


class RecipeTest(TestCase):
    def setUp(self) -> None:
        self.recipe: Recipe = baker.make(
            'recipes.Recipe',
            make_m2m=True,
        )

    def test_recipe_creation(self) -> None:
        """Проверка создания ингредиента и корректность метода __str__."""

        self.assertTrue(isinstance(self.recipe, Recipe))
        self.assertEqual(str(self.recipe), f'{self.recipe.name}'.strip())

        recipe_ingredient = self.recipe.recipe_ingredients.first()
        self.assertEqual(
            str(recipe_ingredient),
            f'{recipe_ingredient.recipe}: {recipe_ingredient.ingredient.name} {recipe_ingredient.quantity}'.strip(),
        )
