from djet import assertions
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.users.api.serializers import UserSerializer
from apps.users.models import CustomUser

from ...factories import login_user
from ...factories import UserFactory


class UserViewSetDetailTest(
    APITestCase, assertions.StatusCodeAssertionsMixin,
):
    def setUp(self) -> None:
        super().setUp()
        self.current_user: CustomUser = UserFactory.create()
        self.user: CustomUser = UserFactory.create()
        self.base_url = 'api:users-detail'

    def test_unauthenticated_user_cannot_get_user_detail(self) -> None:
        """Проверка получения профиля пользователя неавторизованным пользователем"""

        response = self.client.get(
            reverse(
                self.base_url,
                args=[self.user.pk],
            ),
        )

        self.assert_status_equal(response, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_get_other_user_detail(self) -> None:
        """Проверка успешного получения профиля пользователя"""

        login_user(self.client, self.user)

        response = self.client.get(
            reverse(
                self.base_url,
                args=[self.user.pk],
            ),
        )
        response.user = self.current_user

        self.assert_status_equal(response, status.HTTP_200_OK)

        user = CustomUser.objects.get(pk=self.user.pk)

        serializer = UserSerializer(
            user,
            context={'request': response},
        )

        self.assertEqual(response.data, serializer.data)

    def test_user_try_get_non_existent_user_detail(self) -> None:
        """Проверка получения профиля несуществующего пользователя"""

        login_user(self.client, self.user)

        incorrect_user_id = 999
        response = self.client.get(
            reverse(
                self.base_url,
                args=[incorrect_user_id],
            ),
        )

        self.assert_status_equal(response, status.HTTP_404_NOT_FOUND)
        self.assertFalse(
            CustomUser.objects.filter(pk=incorrect_user_id).exists(),
        )
