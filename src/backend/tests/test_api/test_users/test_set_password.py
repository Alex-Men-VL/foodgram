from djet import assertions
from djoser.conf import settings as djoser_settings
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.users.models import CustomUser

from ...factories import login_user
from ...factories import UserFactory

Token = djoser_settings.TOKEN_MODEL


class UserViewSetCreateTest(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
    assertions.InstanceAssertionsMixin,
):
    def setUp(self) -> None:
        super().setUp()
        self.base_url = 'api:users-set-password'
        self.user: CustomUser = UserFactory.create(password='secret_password')

    def test_post_set_new_password(self) -> None:
        """Проверка успешного изменения пароля"""

        self.assert_instance_exists(get_user_model(), pk=self.user.pk)
        user = CustomUser.objects.get(pk=self.user.pk)

        login_user(self.client, user)

        data = {
            'new_password': 'new_secret_password',
            'current_password': 'secret_password',
        }
        response = self.client.post(
            reverse(self.base_url),
            data,
        )
        self.assert_status_equal(response, status.HTTP_204_NO_CONTENT)

        user.refresh_from_db()
        self.assertTrue(user.check_password(data['new_password']))

    def test_post_logout_after_password_change(self) -> None:
        """Проверка, что пользователь вышел из системы после смены пароля"""

        self.assert_instance_exists(get_user_model(), pk=self.user.pk)
        user = CustomUser.objects.get(pk=self.user.pk)

        login_user(self.client, user)

        data = {
            'new_password': 'new_secret_password',
            'current_password': 'secret_password',
        }
        response = self.client.post(
            reverse(self.base_url),
            data,
        )
        self.assert_status_equal(response, status.HTTP_204_NO_CONTENT)
        is_logged = Token.objects.filter(user=user).exists()
        self.assertFalse(is_logged)

    def test_post_not_set_new_password_if_fails_validation(self) -> None:
        """Проверка неудачной смены пароля, если новый пароль не валиден"""

        self.assert_instance_exists(get_user_model(), pk=self.user.pk)
        user = CustomUser.objects.get(pk=self.user.pk)

        login_user(self.client, user)

        data = {'new_password': '123', 'current_password': 'secret_password'}
        response = self.client.post(
            reverse(self.base_url),
            data,
        )

        self.assert_status_equal(response, status.HTTP_400_BAD_REQUEST)

        response.render()
        self.assertEqual(
            str(response.data['new_password'][0]),
            'Введённый пароль слишком короткий. Он должен содержать как минимум 8 символов.',
        )
