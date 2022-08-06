from django.test import TestCase

from apps.recipes.api.serializers import RecipeIngredientFlatRetrieveSerializer
from apps.recipes.models import Recipe
from apps.recipes.models import RecipeIngredient

from ...factories import RecipeFactory
from ...factories import RecipeIngredientFactory


class RecipeIngredientFlatRetrieveSerializerTest(TestCase):
    def setUp(self) -> None:
        self.recipe: Recipe = RecipeFactory.create()
        self.recipe_ingredient: RecipeIngredient = RecipeIngredientFactory.create(recipe=self.recipe)

        self.expected_data = {
            'id': self.recipe_ingredient.ingredient.pk,
            'name': self.recipe_ingredient.ingredient.name,
            'measurement_unit': self.recipe_ingredient.ingredient.measurement_unit,
            'amount': self.recipe_ingredient.amount,
        }
        self.serializer = RecipeIngredientFlatRetrieveSerializer(self.recipe_ingredient)

    def test_contains_expected_fields_keys(self) -> None:
        """Проверка, что сериализатор возвращает корректные ключи"""

        data = self.serializer.data
        self.assertEqual(data.keys(), self.expected_data.keys())

    def test_contains_expected_fields_values(self) -> None:
        """Проверка, что сериализатор возвращает корректные значение"""

        data = self.serializer.data
        self.assertEqual(set(data.values()), set(self.expected_data.values()))
