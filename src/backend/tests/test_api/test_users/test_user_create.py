from djet import assertions
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.users.models import CustomUser

from ...factories import UserFactory


class UserViewSetCreateTest(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
    assertions.InstanceAssertionsMixin,
):
    def setUp(self) -> None:
        super().setUp()
        self.base_url = 'api:users-list'

    def test_post_create_user(self) -> None:
        """Проверка успешной регистрации пользователя"""

        user = UserFactory.build()
        data = {
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'password': user.password,
        }

        self.assert_instance_does_not_exist(
            get_user_model(),
            username=data['username'],
        )
        response = self.client.post(
            reverse(self.base_url),
            data,
        )
        self.assert_status_equal(response, status.HTTP_201_CREATED)

        self.assertTrue('password' not in response.data)
        self.assert_instance_exists(
            get_user_model(),
            username=data['username'],
        )

        user = CustomUser.objects.get(username=data['username'])
        self.assertTrue(user.check_password(data['password']))
        self.assertTrue(user.is_active)

    def test_post_not_create_new_user_if_username_exists(self) -> None:
        """Проверка неудачной регистрации, если профиль с таким username уже существует"""

        user = UserFactory.create()
        data = {
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'password': user.password,
        }

        self.assert_instance_exists(
            get_user_model(),
            username=data['username'],
        )
        response = self.client.post(
            reverse(self.base_url),
            data,
        )

        self.assert_status_equal(response, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(CustomUser.objects.count(), 1)

    def test_post_not_create_if_fails_password_validation(self) -> None:
        """Проверка неудачной регистрации, если пароль не прошел валидацию"""

        user = UserFactory.build()
        data = {
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'password': '123',
        }
        self.assert_instance_does_not_exist(
            get_user_model(),
            username=data['username'],
        )

        response = self.client.post(
            reverse(self.base_url),
            data,
        )
        self.assert_status_equal(response, status.HTTP_400_BAD_REQUEST)

        response.render()
        self.assertEqual(
            str(response.data['password'][0]),
            'Введённый пароль слишком короткий. Он должен содержать как минимум 8 символов.',
        )

    def test_post_not_create_if_fails_email_validation(self) -> None:
        """Проверка неудачной регистрации, если был введен некорректный email"""

        user = UserFactory.build()
        data = {
            'email': 'wrong',
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'password': user.password,
        }

        response = self.client.post(
            reverse(self.base_url),
            data,
        )
        self.assert_status_equal(response, status.HTTP_400_BAD_REQUEST)

        response.render()
        self.assertEqual(
            str(response.data['email'][0]),
            'Введите правильный адрес электронной почты.',
        )
