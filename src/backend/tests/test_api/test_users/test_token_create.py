import typing

from djet import assertions
from djoser.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import user_logged_in
from django.contrib.auth import user_login_failed
from django.urls import reverse

from apps.users.models import CustomUser

from ...factories import UserFactory


class TokenCreateViewTest(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
    assertions.InstanceAssertionsMixin,
):
    def setUp(self) -> None:
        super().setUp()
        self.base_url = 'api:login'
        self.signal_sent = False
        self.user: CustomUser = UserFactory.create(password='secret_password')
        self.raw_password = 'secret_password'

    def signal_receiver(
        self,
        *args: typing.List,
        **kwargs: typing.Dict,
    ) -> None:
        self.signal_sent = True

    def test_post_should_login_user(self) -> None:
        """Проверка, что после получения токена, пользователь становится авторизованным"""

        previous_last_login = self.user.last_login

        data = {'email': self.user.email, 'password': self.raw_password}
        user_logged_in.connect(self.signal_receiver)
        user = CustomUser.objects.get(pk=self.user.pk)

        response = self.client.post(
            reverse(self.base_url),
            data,
        )
        user.refresh_from_db()

        self.assert_status_equal(response, status.HTTP_200_OK)

        self.assertEqual(response.data['auth_token'], user.auth_token.key)
        self.assertNotEqual(user.last_login, previous_last_login)
        self.assertTrue(self.signal_sent)

    def test_post_should_not_login_if_invalid_credentials(self) -> None:
        """Проверка, что пользователь не становится авторизованным, если ввел некорректные данные"""

        data = {'username': self.user.username, 'password': 'wrong'}
        user_login_failed.connect(self.signal_receiver)

        response = self.client.post(
            reverse(self.base_url),
            data,
        )

        self.assert_status_equal(response, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['non_field_errors'],
            [settings.CONSTANTS.messages.INVALID_CREDENTIALS_ERROR],
        )
        self.assertTrue(self.signal_sent)

    def test_post_should_not_login_if_empty_request(self) -> None:
        """Проверка, что пользователь не становится авторизованным, если не ввел данные"""

        data: typing.Dict = {}

        response = self.client.post(
            reverse(self.base_url),
            data,
        )

        self.assert_status_equal(response, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['non_field_errors'],
            [settings.CONSTANTS.messages.INVALID_CREDENTIALS_ERROR],
        )
