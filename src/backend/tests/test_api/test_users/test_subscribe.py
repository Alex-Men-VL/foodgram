from djet import assertions
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.subscriptions.models import Subscription
from apps.users.api.serializers import UserSubscriptionSerializer
from apps.users.models import CustomUser

from ...factories import login_user
from ...factories import UserFactory


class UserViewSetSubscribeTest(
    APITestCase, assertions.StatusCodeAssertionsMixin,
):
    def setUp(self) -> None:
        super().setUp()
        self.user: CustomUser = UserFactory()
        self.author: CustomUser = UserFactory()
        self.base_url = 'api:users-subscribe'

    def test_successful_subscribe_with_status_201(self) -> None:
        """Проверка успешного оформления подписки"""

        login_user(self.client, self.user)
        response = self.client.get(
            reverse(self.base_url, args=[self.author.pk]),
        )
        response.user = self.user

        self.assert_status_equal(response, status.HTTP_201_CREATED)

        author = CustomUser.objects.get(pk=self.author.pk)
        subscriber = CustomUser.objects.get(pk=self.user.pk)

        serializer = UserSubscriptionSerializer(
            author,
            context={'request': response},
        )
        self.assertEqual(response.data, serializer.data)

        subscriptions = Subscription.objects.all()
        self.assertEqual(subscriptions.count(), 1)
        self.assertTrue(
            subscriptions.filter(author=author, subscriber=subscriber).exists(),
        )

    def test_unsuccessful_subscribe_with_status_400(self) -> None:
        """Проверка неудачного оформления подписки со статусом 400 (ошибка подписки)."""

        login_user(self.client, self.user)

        response = self.client.get(
            reverse('api:users-subscribe', args=[self.author.pk]),
        )
        self.assert_status_equal(response, status.HTTP_201_CREATED)

        response = self.client.get(
            reverse('api:users-subscribe', args=[self.author.pk]),
        )
        self.assert_status_equal(response, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(Subscription.objects.count(), 1)

    def test_unsuccessful_subscribe_with_status_401(self) -> None:
        """Проверка неудачного оформления подписки со статусом 401 (пользователь не авторизован)."""

        response = self.client.get(
            reverse('api:users-subscribe', args=[self.author.pk]),
        )
        self.assert_status_equal(response, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(Subscription.objects.count(), 0)

    def test_unsuccessful_subscribe_with_status_404(self) -> None:
        """Проверка неудачного оформления подписки со статусом 404 (объект не найден)."""

        login_user(self.client, self.user)

        incorrect_user_id = 999
        response = self.client.get(
            reverse('api:users-subscribe', args=[incorrect_user_id]),
        )
        self.assert_status_equal(response, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Subscription.objects.count(), 0)
        self.assertFalse(
            CustomUser.objects.filter(pk=incorrect_user_id).exists(),
        )
