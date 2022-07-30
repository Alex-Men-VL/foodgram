from uuid import UUID

from .models import Subscription


def check_subscription_exist(author_uuid: UUID, user_uuid: UUID) -> bool:
    """Проверка наличия подписки на пользователя.

    :param author_uuid: UUID пользователя, наличие подписки на которого проверяется.
    :param user_uuid: UUID пользователя, у которого проверяется наличие подписки.

    :return: True, если подписка есть, иначе - False.
    """

    subscription = Subscription.objects.select_related(
        'author',
        'subscriber',
    ).filter(
        author__uuid=author_uuid,
        subscriber__uuid=user_uuid,
    )
    return subscription.exists()
