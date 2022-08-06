from djet import assertions
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.favourites.api.serializers import FavouriteSerializer
from apps.favourites.models import Favourite
from apps.favourites.selectors import get_favourite
from apps.recipes.models import Recipe
from apps.users.models import CustomUser

from ...factories import FavouriteFactory
from ...factories import login_user
from ...factories import RecipeFactory
from ...factories import UserFactory


class RecipeViewSetFavoriteTest(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
    assertions.InstanceAssertionsMixin,
):
    def setUp(self) -> None:
        super().setUp()
        self.user: CustomUser = UserFactory()
        self.recipe: Recipe = RecipeFactory.create(
            image=None,
        )
        self.base_url = 'api:recipes-favorite'

    def test_unauthenticated_user_cannot_add_recipe_to_favorite(self) -> None:
        """Проверка, что неавторизованный пользователь не может добавить рецепт в избранное"""

        response = self.client.get(
            reverse(
                self.base_url,
                args=[self.recipe.pk],
            ),
        )
        self.assert_status_equal(response, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_remove_recipe_from_favorite(self) -> None:
        """Проверка, что неавторизованный пользователь не может удалить рецепт в избранного"""

        response = self.client.delete(
            reverse(
                self.base_url,
                args=[self.recipe.pk],
            ),
        )
        self.assert_status_equal(response, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_add_recipe_to_favorite(self) -> None:
        """Проверка, что пользователь может добавить рецепт в избранное"""

        login_user(self.client, self.user)

        response = self.client.get(
            reverse(
                self.base_url,
                args=[self.recipe.pk],
            ),
        )
        self.assert_status_equal(response, status.HTTP_201_CREATED)

        favourite = get_favourite(self.user.pk, self.recipe.pk)
        self.assertIsNotNone(favourite)

        serializer = FavouriteSerializer(favourite)
        self.assertEqual(response.data, serializer.data)

    def test_user_cannot_add_recipe_to_favorite_twice(self) -> None:
        """Проверка, что пользователь не может добавить рецепт в избранное дважды"""

        login_user(self.client, self.user)
        favourite = FavouriteFactory.create(
            user=self.user,
            recipe=self.recipe,
        )

        self.assert_instance_exists(
            Favourite,
            pk=favourite.pk,
        )

        response = self.client.get(
            reverse(
                self.base_url,
                args=[self.recipe.pk],
            ),
        )
        self.assert_status_equal(response, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_add_non_existing_recipe_to_favorite(self) -> None:
        """Проверка, что пользователь не может добавить несуществующий рецепт в избранное"""

        login_user(self.client, self.user)
        incorrect_recipe_id = 999

        self.assert_instance_does_not_exist(
            Favourite,
            user=self.user,
            recipe_id=incorrect_recipe_id,
        )

        response = self.client.get(
            reverse(
                self.base_url,
                args=[incorrect_recipe_id],
            ),
        )
        self.assert_status_equal(response, status.HTTP_404_NOT_FOUND)

    def test_user_can_remove_recipe_from_favourite(self) -> None:
        """Проверка, что пользователь может удалить рецепт из избранного"""

        login_user(self.client, self.user)
        favourite = FavouriteFactory.create(
            user=self.user,
            recipe=self.recipe,
        )

        self.assert_instance_exists(
            Favourite,
            pk=favourite.pk,
        )

        response = self.client.delete(
            reverse(
                self.base_url,
                args=[self.recipe.pk],
            ),
        )
        self.assert_status_equal(response, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_remove_not_added_recipe_from_favourite(self) -> None:
        """Проверка, что пользователь не может удалить рецепт из избранного, если он не был добавлен заранее"""

        login_user(self.client, self.user)

        response = self.client.delete(
            reverse(
                self.base_url,
                args=[self.recipe.pk],
            ),
        )
        self.assert_status_equal(response, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_remove_non_existing_recipe_to_favorite(self) -> None:
        """Проверка, что пользователь не может удалить несуществующий рецепт в избранное"""

        login_user(self.client, self.user)
        incorrect_recipe_id = 999

        self.assert_instance_does_not_exist(
            Favourite,
            user=self.user,
            recipe_id=incorrect_recipe_id,
        )

        response = self.client.delete(
            reverse(
                self.base_url,
                args=[incorrect_recipe_id],
            ),
        )
        self.assert_status_equal(response, status.HTTP_404_NOT_FOUND)
