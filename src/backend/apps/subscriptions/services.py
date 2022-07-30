import typing
from uuid import UUID

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Subscription

CustomUser = get_user_model()


class SubscriptionService:
    """Сервис для изменения подписки на автора.

    Сервис инкапсулирует два публичных метода:
      - Добавление подписки на автора;
      - Удаление подписки на автора.
    """

    def __init__(self, author_uuid: UUID, subscriber_uuid: UUID) -> None:
        self.author = get_object_or_404(CustomUser, uuid=author_uuid)
        self.subscriber = get_object_or_404(CustomUser, uuid=subscriber_uuid)

    def add_subscription(self) -> typing.Tuple[Subscription, bool]:
        """Добавление подписки на пользователя.

        :return: Кортеж из двух элементов: экземпляр модели `Subscription` и статус True, если подписка создана,
            или False, если подписка уже существовала
        """

        subscription, created = Subscription.objects.get_or_create(
            author=self.author,
            subscriber=self.subscriber,
        )
        return subscription, created

    def dell_subscription(self) -> bool:
        """Удаление подписки на пользователя.

        :return: Результат операции: True, если подписка удалена, False, если подписки не было
        """

        deleted, _ = Subscription.objects.filter(
            author=self.author,
            subscriber=self.subscriber,
        ).delete()
        return deleted
