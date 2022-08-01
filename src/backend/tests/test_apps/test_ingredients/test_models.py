from django.db import IntegrityError
from django.test import TestCase

from apps.ingredients.models import Ingredient

from ...factories import IngredientFactory


class IngredientTest(TestCase):
    def setUp(self) -> None:
        self.ingredient: Ingredient = IngredientFactory()

    def test_ingredient_creation(self) -> None:
        """Проверка создания ингредиента и корректность метода __str__."""

        self.assertTrue(isinstance(self.ingredient, Ingredient))
        self.assertEqual(
            str(self.ingredient),
            f'{self.ingredient.name}, {self.ingredient.measurement_unit}'.strip(),
        )

    def test_name_measurement_unit_unique_together(self) -> None:
        """Проверка совместной уникальности полей name и measurement_unit."""

        with self.assertRaises(IntegrityError):
            IngredientFactory.create_batch(
                name='Сахар',
                measurement_unit='г',
                size=2,
            )
