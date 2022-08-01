from factory import SubFactory
from factory.django import DjangoModelFactory

from apps.subscriptions.models import Subscription

from .user_factory import UserFactory


class SubscriptionFactory(DjangoModelFactory):

    subscriber = SubFactory(UserFactory)
    author = SubFactory(UserFactory)

    class Meta:
        model = Subscription
