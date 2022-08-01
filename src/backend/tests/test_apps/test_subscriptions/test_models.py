from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from apps.subscriptions.models import Subscription
from apps.users.models import CustomUser

from ...factories import SubscriptionFactory
from ...factories import UserFactory


class SubscriptionTest(TestCase):
    def setUp(self) -> None:
        self.subscriber: CustomUser = UserFactory()
        self.author: CustomUser = UserFactory()
        self.subscription: Subscription = SubscriptionFactory(
            subscriber=self.subscriber,
            author=self.author,
        )

    def test_subscription_creation(self) -> None:
        """Проверка создания подписки и корректность метода __str__."""

        self.assertEqual(self.subscription.author, self.author)
        self.assertEqual(self.subscription.subscriber, self.subscriber)

        self.assertTrue(isinstance(self.subscription, Subscription))
        self.assertEqual(
            str(self.subscription),
            f'{self.subscription.subscriber.full_name}: {self.subscription.author.full_name}',
        )

    def test_author_recipe_unique_together(self) -> None:
        """Проверка совместной уникальности полей subscriber и author."""

        with self.assertRaises(IntegrityError):
            SubscriptionFactory.create_batch(
                subscriber=self.subscriber,
                author=self.author,
                size=2,
            )

    def test_not_allow_self_following(self) -> None:
        """Проверка невозможности подписаться на самого себя."""

        subscription: Subscription = SubscriptionFactory.build(
            subscriber=self.author,
            author=self.author,
        )

        with self.assertRaises(ValidationError):
            subscription.full_clean()
