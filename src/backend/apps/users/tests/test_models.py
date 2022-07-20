from model_bakery import baker

from django.test import TestCase

from ..models import CustomUser


class CustomUserTest(TestCase):
    def setUp(self) -> None:
        self.user: CustomUser = baker.make(
            'users.CustomUser',
        )

    def test_user_creation(self) -> None:
        """Проверка создания пользователя и корректность метода __str__."""

        self.assertTrue(isinstance(self.user, CustomUser))
        self.assertEqual(
            str(self.user),
            f'{self.user.first_name} {self.user.last_name}'.strip(),
        )
