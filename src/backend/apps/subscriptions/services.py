import typing

from ..users.models import CustomUser
from .models import Subscription


class SubscriptionService:
    """Сервис для изменения подписки на автора"""

    def __init__(self, author: CustomUser, subscriber: CustomUser) -> None:
        self.author: CustomUser = author
        self.subscriber: CustomUser = subscriber

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
