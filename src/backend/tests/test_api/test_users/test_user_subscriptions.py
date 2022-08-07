from djet import assertions
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.recipes.models import Recipe
from apps.subscriptions.models import Subscription
from apps.subscriptions.selectors import get_user_subscriptions_authors
from apps.users.api.serializers import UserSubscriptionSerializer
from apps.users.models import CustomUser

from ...factories import login_user
from ...factories import RecipeFactory
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

        self.author: CustomUser = UserFactory.create()
        self.author_recipes: Recipe = RecipeFactory.create_batch(
            author=self.author,
            size=3,
        )
        self.custom_subscription: Subscription = SubscriptionFactory.create(
            subscriber=self.user,
            author=self.author,
        )
        self.subscriptions_number += 1

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
        response_subscriptions = response.json()['results']

        self.assertEqual(len(response_subscriptions), self.subscriptions_number)
        self.assertEqual(response_subscriptions, serializer.data)
        self.assertTrue(
            all(
                subscription['is_subscribed']
                for subscription in response_subscriptions
            ),
        )

    def test_user_can_get_subscriptions_with_page_size_limit(self) -> None:
        """Проверка успешного получения пользователем списка пользователей, на которых он подписан,
        с установленным лимитом подписок
        """

        login_user(self.client, self.user)

        page_size_limit = 1
        page_number = 2
        response = self.client.get(
            f'{reverse(self.base_url)}?limit={page_size_limit}&page={page_number}',
        )
        self.assert_status_equal(response, status.HTTP_200_OK)

        self.assertIsNotNone(response.json()['next'])
        self.assertIsNotNone(response.json()['previous'])

        response_subscriptions = response.json()['results']
        self.assertEqual(len(response_subscriptions), page_size_limit)

    def test_user_can_get_subscriptions_with_recipes_limit(self) -> None:
        """Проверка успешного получения пользователем списка пользователей, на которых он подписан,
        с установленным лимитом на количество рецептов
        """

        login_user(self.client, self.user)

        recipes_limit = 1
        response = self.client.get(
            f'{reverse(self.base_url)}?recipes_limit={recipes_limit}',
        )
        self.assert_status_equal(response, status.HTTP_200_OK)

        response_subscriptions = response.json()['results']
        self.assertTrue(
            all(
                len(subscription['recipes']) <= recipes_limit
                for subscription in response_subscriptions
            ),
        )
