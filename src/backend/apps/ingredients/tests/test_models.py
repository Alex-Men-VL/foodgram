from model_bakery import baker

from django.db import IntegrityError
from django.test import TestCase

from ..models import Ingredient


class IngredientTest(TestCase):

    def setUp(self) -> None:
        self.ingredient: Ingredient = baker.make('ingredients.Ingredient')

    def test_ingredient_creation(self) -> None:
        """Проверка создания ингредиента и корректность метода __str__."""

        self.assertTrue(isinstance(self.ingredient, Ingredient))
        self.assertEqual(str(self.ingredient), f'{self.ingredient.title}, {self.ingredient.unit}'.strip())

    def test_title_unit_unique_together(self) -> None:
        """Проверка совместной уникальности полей title и unit."""

        with self.assertRaises(IntegrityError):
            baker.make(
                'ingredients.Ingredient',
                title='Помидор',
                unit='г',
                _quantity=2,
            )
