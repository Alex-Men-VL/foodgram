from djet import assertions
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.recipes.models import Recipe
from apps.users.models import CustomUser

from ...factories import login_user
from ...factories import RecipeFactory
from ...factories import UserFactory


class RecipeViewSetUpdateTest(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
    assertions.InstanceAssertionsMixin,
):
    def setUp(self) -> None:
        super().setUp()
        self.user: CustomUser = UserFactory.create()
        self.recipe: Recipe = RecipeFactory()
        self.user_recipe: Recipe = RecipeFactory(author=self.user)
        self.base_url = 'api:recipes-detail'

    def test_non_recipe_author_cannot_edit_recipe(self) -> None:
        """Проверка только автор рецепта может изменить свой рецепт"""

        login_user(self.client, self.user)
        new_recipe_name = 'new name'

        response = self.client.patch(
            reverse(
                self.base_url,
                args=[self.recipe.pk],
            ),
            data={
                'name': new_recipe_name,
            },
        )
        self.assert_status_equal(response, status.HTTP_403_FORBIDDEN)

    def test_user_author_can_update_recipe(self) -> None:
        """Проверка успешного изменения рецепта автором"""

        login_user(self.client, self.user)
        new_recipe_name = 'new name'

        response = self.client.patch(
            reverse(
                self.base_url,
                args=[self.user_recipe.pk],
            ),
            data={
                'name': new_recipe_name,
            },
        )
        self.assert_status_equal(response, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], new_recipe_name)
