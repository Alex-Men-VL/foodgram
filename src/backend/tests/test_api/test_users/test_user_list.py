from djet import assertions
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.users.api.serializers import UserSerializer
from apps.users.models import CustomUser

from ...factories import login_user
from ...factories import UserFactory


class UserViewSetListTest(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
):
    def setUp(self) -> None:
        super().setUp()
        self.current_user: CustomUser = UserFactory.create()
        self.user: CustomUser = UserFactory.create()
        self.base_url = 'api:users-list'

    def test_unauthenticated_user_cannot_list_users(self) -> None:
        """Проверка получения списка пользователя неавторизованным пользователем"""

        response = self.client.get(
            reverse(self.base_url),
        )

        self.assert_status_equal(response, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_list_users(self) -> None:
        """Проверка успешного получения списка пользователей"""

        login_user(self.client, self.current_user)

        response = self.client.get(
            reverse(self.base_url),
        )
        response.user = self.current_user

        self.assert_status_equal(response, status.HTTP_200_OK)

        total_users_number = CustomUser.objects.count()
        self.assertEqual(total_users_number, 2)

        users = CustomUser.objects.get_with_subscription_status(
            subscriber_id=self.current_user,
        )

        serializer = UserSerializer(
            users,
            many=True,
        )

        self.assertEqual(len(response.json()), total_users_number)
        self.assertEqual(response.json(), serializer.data)
