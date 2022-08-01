from django.test import TestCase

from apps.carts.models import Cart
from apps.users.models import CustomUser

from ..factories import CartFactory
from ..factories import UserFactory


class CartTest(TestCase):
    def setUp(self) -> None:
        self.user: CustomUser = UserFactory()
        self.cart: Cart = CartFactory(owner=self.user)

    def test_cart_creation(self) -> None:
        """Проверка создания списка покупок и корректность метода __str__."""

        self.assertEqual(self.cart.owner, self.user)

        self.assertTrue(isinstance(self.cart, Cart))
        self.assertEqual(
            str(self.cart),
            f'Список покупок: {self.cart.owner.full_name}',
        )
