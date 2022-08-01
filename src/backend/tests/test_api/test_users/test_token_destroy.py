import typing

from djet import assertions
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import user_logged_out
from django.urls import reverse

from apps.users.models import CustomUser

from ...factories import login_user
from ...factories import UserFactory


class TokenDestroyViewTest(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
    assertions.InstanceAssertionsMixin,
):
    def setUp(self) -> None:
        super().setUp()
        self.base_url = 'api:logout'
        self.signal_sent = False
        self.user: CustomUser = UserFactory.create(password='secret_password')
        self.raw_password = 'secret_password'

    def signal_receiver(
        self,
        *args: typing.List,
        **kwargs: typing.Dict,
    ) -> None:
        self.signal_sent = True

    def test_post_should_logout_logged_in_user(self) -> None:
        """Проверка, что пользователь выходит из системы"""

        user_logged_out.connect(self.signal_receiver)

        login_user(self.client, self.user)
        response = self.client.post(reverse(self.base_url))

        self.assert_status_equal(response, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
        self.assertTrue(self.signal_sent)

    def test_post_should_deny_logging_out_when_user_not_logged_in(
        self,
    ) -> None:
        """Проверка неудачного запроса, не пользователь не авторизован"""

        response = self.client.post(reverse(self.base_url))

        self.assert_status_equal(response, status.HTTP_401_UNAUTHORIZED)
