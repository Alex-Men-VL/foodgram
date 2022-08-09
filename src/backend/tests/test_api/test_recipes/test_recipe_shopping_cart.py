from djet import assertions
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.carts.selectors import get_cart_recipe
from apps.recipes.api.serializers import ShortRecipeSerializer
from apps.recipes.models import Recipe
from apps.users.models import CustomUser

from ...factories import CartFactory
from ...factories import login_user
from ...factories import RecipeFactory
from ...factories import UserFactory


class RecipeViewSetShoppingCartTest(
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
        self.base_url = 'api:recipes-shopping-cart'

    def test_unauthenticated_user_cannot_add_recipe_to_shopping_cart(self) -> None:
        """Проверка, что неавторизованный пользователь не может добавить рецепт в список покупок"""

        response = self.client.get(
            reverse(
                self.base_url,
                args=[self.recipe.pk],
            ),
        )
        self.assert_status_equal(response, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_remove_recipe_from_shopping_cart(self) -> None:
        """Проверка, что неавторизованный пользователь не может удалить рецепт из списка покупок"""

        response = self.client.delete(
            reverse(
                self.base_url,
                args=[self.recipe.pk],
            ),
        )
        self.assert_status_equal(response, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_add_recipe_to_shopping_cart(self) -> None:
        """Проверка, что пользователь может добавить рецепт в список покупок"""

        login_user(self.client, self.user)

        response = self.client.get(
            reverse(
                self.base_url,
                args=[self.recipe.pk],
            ),
        )
        self.assert_status_equal(response, status.HTTP_201_CREATED)

        recipe = get_cart_recipe(self.user.pk, self.recipe.pk)
        self.assertIsNotNone(recipe)

        serializer = ShortRecipeSerializer(recipe)
        self.assertEqual(response.data, serializer.data)

    def test_user_cannot_add_recipe_to_shopping_cart_twice(self) -> None:
        """Проверка, что пользователь не может добавить рецепт в список покупок дважды"""

        login_user(self.client, self.user)
        cart = CartFactory.create(
            owner=self.user,
            recipes=[
                self.recipe,
            ],
        )
        self.assertTrue(cart.recipes.filter(pk=self.recipe.pk).exists())

        response = self.client.get(
            reverse(
                self.base_url,
                args=[self.recipe.pk],
            ),
        )
        self.assert_status_equal(response, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_add_non_existing_recipe_to_shopping_cart(self) -> None:
        """Проверка, что пользователь не может добавить несуществующий рецепт в список покупок"""

        login_user(self.client, self.user)
        incorrect_recipe_id = 999

        self.assert_instance_does_not_exist(
            Recipe,
            pk=incorrect_recipe_id,
        )

        response = self.client.get(
            reverse(
                self.base_url,
                args=[incorrect_recipe_id],
            ),
        )
        self.assert_status_equal(response, status.HTTP_404_NOT_FOUND)

    def test_user_can_remove_recipe_from_shopping_cart(self) -> None:
        """Проверка, что пользователь может удалить рецепт из списка покупок"""

        login_user(self.client, self.user)
        cart = CartFactory.create(
            owner=self.user,
            recipes=[
                self.recipe,
            ],
        )

        self.assertTrue(cart.recipes.filter(pk=self.recipe.pk).exists())

        response = self.client.delete(
            reverse(
                self.base_url,
                args=[self.recipe.pk],
            ),
        )
        self.assert_status_equal(response, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_remove_not_added_recipe_from_shopping_cart(self) -> None:
        """Проверка, что пользователь не может удалить рецепт из списка покупок, если он не был добавлен заранее"""

        login_user(self.client, self.user)

        response = self.client.delete(
            reverse(
                self.base_url,
                args=[self.recipe.pk],
            ),
        )
        self.assert_status_equal(response, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_remove_non_existing_recipe_to_shopping_cart(self) -> None:
        """Проверка, что пользователь не может удалить несуществующий рецепт из списка покупок"""

        login_user(self.client, self.user)
        incorrect_recipe_id = 999
        cart = CartFactory.create(
            owner=self.user,
        )

        self.assertFalse(cart.recipes.filter(pk=self.recipe.pk).exists())

        response = self.client.delete(
            reverse(
                self.base_url,
                args=[incorrect_recipe_id],
            ),
        )
        self.assert_status_equal(response, status.HTTP_404_NOT_FOUND)
