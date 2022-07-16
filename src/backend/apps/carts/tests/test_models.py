from model_bakery import baker

from django.test import TestCase

from ..models import Cart


class CartTest(TestCase):

    def setUp(self) -> None:
        self.cart: Cart = baker.make('carts.Cart')

    def test_cart_creation(self) -> None:
        """Проверка создания списка покупок и корректность метода __str__."""

        self.assertTrue(isinstance(self.cart, Cart))
        self.assertEqual(
            str(self.cart),
            f'{self.cart.owner.full_name}',
        )
