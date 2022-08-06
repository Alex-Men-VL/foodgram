from djet import assertions
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.recipes.api.serializers import RecipeRetrieveSerializer
from apps.recipes.models import Recipe
from apps.recipes.selectors import get_recipes_for_current_user
from apps.users.models import CustomUser

from ...factories import RecipeFactory
from ...factories import UserFactory


class RecipeViewSetDetailTest(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
    assertions.InstanceAssertionsMixin,
):
    def setUp(self) -> None:
        super().setUp()
        self.user: CustomUser = UserFactory.create()
        self.recipe: Recipe = RecipeFactory.create(
            image=None,
        )
        self.base_url = 'api:recipes-detail'

    def test_user_can_get_recipe_detail(self) -> None:
        """Проверка успешного получения определенного рецепта"""

        response = self.client.get(
            reverse(
                self.base_url,
                args=[self.recipe.pk],
            ),
        )
        self.assert_status_equal(response, status.HTTP_200_OK)

        recipe = get_recipes_for_current_user(
            self.user.pk,
            self.recipe.pk,
        )
        serializer = RecipeRetrieveSerializer(recipe)

        self.assertEqual(response.data, serializer.data)

    def test_user_try_get_non_existent_recipe_detail(self) -> None:
        """Проверка получения несуществующего рецепта"""

        incorrect_recipe_id = 999
        response = self.client.get(
            reverse(
                self.base_url,
                args=[incorrect_recipe_id],
            ),
        )

        self.assert_status_equal(response, status.HTTP_404_NOT_FOUND)
        self.assert_instance_does_not_exist(CustomUser, pk=incorrect_recipe_id)
