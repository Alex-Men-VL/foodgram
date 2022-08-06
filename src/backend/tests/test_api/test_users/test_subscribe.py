from djet import assertions
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.subscriptions.models import Subscription
from apps.users.api.serializers import UserSubscriptionSerializer
from apps.users.models import CustomUser
from apps.users.selectors import get_current_author
from apps.users.selectors import get_current_user

from ...factories import login_user
from ...factories import SubscriptionFactory
from ...factories import UserFactory


class UserViewSetSubscribeTest(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
    assertions.InstanceAssertionsMixin,
):
    def setUp(self) -> None:
        super().setUp()
        self.user: CustomUser = UserFactory()
        self.author: CustomUser = UserFactory()
        self.base_url = 'api:users-subscribe'

    def test_user_can_subscribe_on_other_user(self) -> None:
        """Проверка успешного оформления подписки"""

        login_user(self.client, self.user)

        response = self.client.get(
            reverse(self.base_url, args=[self.author.pk]),
        )
        response.user = self.user

        self.assert_status_equal(response, status.HTTP_201_CREATED)

        author = get_current_author(self.author.pk, self.user.pk)
        subscriber = get_current_user(self.user.pk)

        serializer = UserSubscriptionSerializer(author)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.data['is_subscribed'], True)

        subscriptions = Subscription.objects.all()
        self.assertEqual(subscriptions.count(), 1)
        self.assert_instance_exists(
            Subscription,
            author=author,
            subscriber=subscriber,
        )

    def test_user_cannot_subscribe_twice_on_one_user(self) -> None:
        """Проверка, что пользователь не может повторно подписаться на одного и того же человека"""

        login_user(self.client, self.user)

        response = self.client.get(
            reverse(self.base_url, args=[self.author.pk]),
        )
        self.assert_status_equal(response, status.HTTP_201_CREATED)

        response = self.client.get(
            reverse(self.base_url, args=[self.author.pk]),
        )
        self.assert_status_equal(response, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(Subscription.objects.count(), 1)

    def test_unauthenticated_user_cannot_subscribe_on_other_user(self) -> None:
        """Проверка, что неавторизованный пользователь не может оформить подписку"""

        response = self.client.get(
            reverse(self.base_url, args=[self.author.pk]),
        )
        self.assert_status_equal(response, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(Subscription.objects.count(), 0)

    def test_user_cannot_subscribe_on_non_existent_user(self) -> None:
        """Проверка, что пользователь не может подписаться на несуществующего пользователя"""

        login_user(self.client, self.user)

        incorrect_user_id = 999
        response = self.client.get(
            reverse(self.base_url, args=[incorrect_user_id]),
        )
        self.assert_status_equal(response, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Subscription.objects.count(), 0)
        self.assert_instance_does_not_exist(
            CustomUser,
            pk=incorrect_user_id,
        )

    def test_user_can_unsubscribe_from_user(self) -> None:
        """Проверка успешного удаления подписки"""

        login_user(self.client, self.user)

        subscription = SubscriptionFactory.create(
            subscriber=self.user,
            author=self.author,
        )
        self.assert_instance_exists(
            Subscription,
            pk=subscription.pk,
        )

        response = self.client.delete(
            reverse(self.base_url, args=[self.author.pk]),
        )

        self.assert_status_equal(response, status.HTTP_204_NO_CONTENT)
        self.assert_instance_does_not_exist(
            Subscription,
            pk=subscription.pk,
        )

    def test_user_can_unsubscribe_if_no_subscription(self) -> None:
        """Проверка, что пользователь не может отписаться, если не подписан"""

        login_user(self.client, self.user)

        self.assert_instance_does_not_exist(
            Subscription,
            subscriber=self.user,
            author=self.author,
        )

        response = self.client.delete(
            reverse(self.base_url, args=[self.author.pk]),
        )

        self.assert_status_equal(response, status.HTTP_400_BAD_REQUEST)

        response.render()
        self.assertEqual(
            str(response.data['errors']),
            'Пользователь не был подписан на этого автора',
        )
