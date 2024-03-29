from djet import assertions
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.users.api.serializers import UserSerializer
from apps.users.models import CustomUser

from ...factories import login_user
from ...factories import UserFactory


class UserViewSetDetailTest(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
    assertions.InstanceAssertionsMixin,
):
    def setUp(self) -> None:
        super().setUp()
        self.current_user: CustomUser = UserFactory.create()
        self.user: CustomUser = UserFactory.create()
        self.base_url = 'api:users-detail'

    def test_unauthenticated_user_can_get_user_detail(self) -> None:
        """Проверка получения профиля пользователя неавторизованным пользователем"""

        response = self.client.get(
            reverse(
                self.base_url,
                args=[self.user.pk],
            ),
        )

        self.assert_status_equal(response, status.HTTP_200_OK)
        self.assertFalse(response.data['is_subscribed'])

    def test_user_can_get_other_user_detail(self) -> None:
        """Проверка успешного получения профиля пользователя"""

        login_user(self.client, self.current_user)

        response = self.client.get(
            reverse(
                self.base_url,
                args=[self.user.pk],
            ),
        )

        self.assert_status_equal(response, status.HTTP_200_OK)

        user = CustomUser.objects.get_with_subscription_status(
            subscriber_id=self.current_user,
        ).get(
            pk=self.user.pk,
        )

        serializer = UserSerializer(user)

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
        self.assert_instance_does_not_exist(CustomUser, pk=incorrect_user_id)
