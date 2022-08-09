from djet import assertions
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.carts.models import Cart
from apps.recipes.models import Recipe
from apps.users.models import CustomUser

from ...factories import CartFactory
from ...factories import login_user
from ...factories import RecipeFactory
from ...factories import UserFactory


class RecipeViewSetDownloadShoppingCartTest(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
    assertions.InstanceAssertionsMixin,
):
    def setUp(self) -> None:
        super().setUp()
        self.user: CustomUser = UserFactory()
        self.user_without_cart: CustomUser = UserFactory()
        self.user_with_empty_cart: CustomUser = UserFactory()

        self.recipes: Recipe = RecipeFactory.create_batch(
            image=None,
            size=2,
        )

        self.cart: Cart = CartFactory.create(
            owner=self.user,
            recipes=self.recipes,
        )
        self.empty_cart: Cart = CartFactory.create(
            owner=self.user_with_empty_cart,
        )

        self.base_url = 'api:recipes-download-shopping-cart'

    def test_unauthenticated_user_cannot_download_shopping_cart(self) -> None:
        """Проверка, что неавторизованный пользователь не может скачать список покупок"""

        response = self.client.get(
            reverse(self.base_url),
        )
        self.assert_status_equal(response, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_download_shopping_cart(self) -> None:
        """Проверка, что пользователь может скачать список покупок"""

        login_user(self.client, self.user)

        response = self.client.get(
            reverse(self.base_url),
        )
        self.assert_status_equal(response, status.HTTP_200_OK)
        self.assertTrue('Список покупок' in response.content.decode('utf-8'))

    def test_user_without_cart_cannot_download_shopping_cart(self) -> None:
        """Проверка, что пользователь, у которого нет списка покупок не может скачать список покупок"""

        login_user(self.client, self.user_without_cart)

        response = self.client.get(
            reverse(self.base_url),
        )
        self.assert_status_equal(response, status.HTTP_400_BAD_REQUEST)
        self.assert_instance_does_not_exist(
            Cart,
            owner=self.user_without_cart,
        )

        response.render()
        self.assertEqual(
            str(response.data['errors']),
            'Список покупок пуст',
        )

    def test_user_with_empty_cart_cannot_download_shopping_cart(self) -> None:
        """Проверка, что пользователь, у которого списка покупок пуст не может скачать список покупок"""

        login_user(self.client, self.user_with_empty_cart)

        response = self.client.get(
            reverse(self.base_url),
        )
        self.assert_status_equal(response, status.HTTP_400_BAD_REQUEST)
        self.assert_instance_exists(
            Cart,
            owner=self.user_with_empty_cart,
        )

        response.render()
        self.assertEqual(
            str(response.data['errors']),
            'Список покупок пуст',
        )
