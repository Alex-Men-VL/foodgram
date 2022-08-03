from djet import assertions
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.subscriptions.models import Subscription
from apps.subscriptions.selectors import get_user_subscriptions_authors
from apps.users.api.serializers import UserSubscriptionSerializer
from apps.users.models import CustomUser

from ...factories import login_user
from ...factories import SubscriptionFactory
from ...factories import UserFactory


class UserViewSetSubscriptionsTest(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
    assertions.InstanceAssertionsMixin,
):
    def setUp(self) -> None:
        super().setUp()
        self.user: CustomUser = UserFactory.create()
        self.subscriptions_number = 2
        self.subscriptions: Subscription = SubscriptionFactory.create_batch(
            subscriber=self.user,
            size=self.subscriptions_number,
        )
        self.base_url = 'api:users-subscriptions'

    def test_unauthenticated_user_cannot_get_subscriptions(self) -> None:
        """Проверка, что неавторизованный пользователь не может получить список пользователей, на которых он подписан"""

        response = self.client.get(
            reverse(self.base_url),
        )
        self.assert_status_equal(response, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_get_subscriptions(self) -> None:
        """Проверка успешного получения пользователем списка пользователей, на которых он подписан"""

        login_user(self.client, self.user)

        response = self.client.get(
            reverse(self.base_url),
        )
        self.assert_status_equal(response, status.HTTP_200_OK)

        total_subscriptions_number = self.user.subscriptions.count()
        self.assertEqual(total_subscriptions_number, self.subscriptions_number)

        authors = get_user_subscriptions_authors(self.user)
        serializer = UserSubscriptionSerializer(
            authors,
            many=True,
        )

        self.assertEqual(len(response.json()), self.subscriptions_number)
        self.assertEqual(response.json(), serializer.data)
        self.assertTrue(
            all(
                subscription['is_subscribed']
                for subscription in response.json()
            ),
        )
