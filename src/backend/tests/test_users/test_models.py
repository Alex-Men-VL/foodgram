from django.test import TestCase

from apps.users.models import CustomUser

from ...factories import UserFactory


class CustomUserTest(TestCase):
    def setUp(self) -> None:
        self.user: CustomUser = UserFactory()

    def test_user_creation(self) -> None:
        """Проверка создания пользователя и корректность метода __str__."""

        self.assertTrue(isinstance(self.user, CustomUser))
        self.assertEqual(
            str(self.user),
            f'{self.user.first_name} {self.user.last_name}'.strip(),
        )
