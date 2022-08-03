from djet import assertions
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.ingredients.api.serializers import IngredientSerializer
from apps.ingredients.models import Ingredient

from ...factories import IngredientFactory


class IngredientViewSetDetailTest(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
    assertions.InstanceAssertionsMixin,
):
    def setUp(self) -> None:
        super().setUp()
        self.ingredient: Ingredient = IngredientFactory.create()
        self.base_url = 'api:ingredients-detail'

    def test_user_can_get_ingredient_detail(self) -> None:
        """Проверка успешного получения определенного ингредиента"""

        response = self.client.get(
            reverse(
                self.base_url,
                args=[self.ingredient.pk],
            ),
        )

        self.assert_status_equal(response, status.HTTP_200_OK)
        self.assert_instance_exists(Ingredient, pk=self.ingredient.pk)

        ingredient = Ingredient.objects.get(pk=self.ingredient.pk)
        serializer = IngredientSerializer(
            ingredient,
        )

        self.assertEqual(response.data, serializer.data)

    def test_user_try_get_non_existent_ingredient_detail(self) -> None:
        """Проверка получения несуществующего ингредиента"""

        incorrect_ingredient_id = 999
        response = self.client.get(
            reverse(
                self.base_url,
                args=[incorrect_ingredient_id],
            ),
        )

        self.assert_status_equal(response, status.HTTP_404_NOT_FOUND)
        self.assert_instance_does_not_exist(Ingredient, pk=incorrect_ingredient_id)
