from djet import assertions
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.users.api.serializers import UserSerializer
from apps.users.models import CustomUser

from ...factories import login_user
from ...factories import UserFactory


class UserViewSetMeTest(
    APITestCase, assertions.StatusCodeAssertionsMixin,
):
    def setUp(self) -> None:
        super().setUp()
        self.user: CustomUser = UserFactory.create()
        self.base_url = 'api:users-me'

    def test_unauthenticated_user_cannot_get_own_profile(self) -> None:
        """Проверка получения своего профиля неавторизованным пользователем"""

        response = self.client.get(
            reverse(self.base_url),
        )

        self.assert_status_equal(response, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_get_own_profile(self) -> None:
        """Проверка успешного получения своего профиля пользователем"""

        login_user(self.client, self.user)

        response = self.client.get(
            reverse(self.base_url),
        )
        response.user = self.user

        self.assert_status_equal(response, status.HTTP_200_OK)

        user = CustomUser.objects.get(pk=self.user.pk)

        serializer = UserSerializer(
            user,
            context={'request': response},
        )

        self.assertEqual(response.data, serializer.data)
