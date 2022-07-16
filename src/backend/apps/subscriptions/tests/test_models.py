from model_bakery import baker

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from ...users.models import CustomUser  # Only for type hinting
from ..models import Subscription


class SubscriptionTest(TestCase):

    def setUp(self) -> None:
        self.subscription: Subscription = baker.make('subscriptions.Subscription')

    def test_subscription_creation(self) -> None:
        """Проверка создания подписки и корректность метода __str__."""

        self.assertTrue(isinstance(self.subscription, Subscription))
        self.assertEqual(
            str(self.subscription),
            f'{self.subscription.subscriber.full_name}: {self.subscription.author.full_name}',
        )

    def test_author_recipe_unique_together(self) -> None:
        """Проверка совместной уникальности полей subscriber и author."""

        author: CustomUser = baker.make(settings.AUTH_USER_MODEL)
        subscriber: CustomUser = baker.make(settings.AUTH_USER_MODEL)

        with self.assertRaises(IntegrityError):
            baker.make(
                'subscriptions.Subscription',
                author=author,
                subscriber=subscriber,
                _quantity=2,
            )

    def test_not_allow_self_following(self) -> None:
        """Проверка невозможности подписаться на самого себя."""

        user: CustomUser = baker.make(settings.AUTH_USER_MODEL)
        subscription: Subscription = baker.prepare(
            'subscriptions.Subscription',
            author=user,
            subscriber=user,
        )

        with self.assertRaises(ValidationError):
            subscription.full_clean()
