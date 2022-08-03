from djet import assertions
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.ingredients.api.serializers import IngredientSerializer
from apps.ingredients.models import Ingredient

from ...factories import IngredientFactory


class IngredientViewSetListTest(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
):
    def setUp(self) -> None:
        super().setUp()
        self.total_ingredients_number = 3
        self.ingredients: Ingredient = IngredientFactory.create_batch(size=self.total_ingredients_number)
        self.base_url = 'api:ingredients-list'

    def test_user_can_list_ingredients(self) -> None:
        """Проверка успешного получения списка тегов"""

        response = self.client.get(
            reverse(self.base_url),
        )

        self.assert_status_equal(response, status.HTTP_200_OK)

        ingredients = Ingredient.objects.all()
        total_ingredients_number = ingredients.count()

        self.assertEqual(total_ingredients_number, self.total_ingredients_number)

        serializer = IngredientSerializer(
            ingredients,
            many=True,
        )

        self.assertEqual(len(response.json()), self.total_ingredients_number)
        self.assertEqual(response.json(), serializer.data)
