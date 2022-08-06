import typing

from django.db.models import BigAutoField
from django.db.models import QuerySet
from django.db.models.expressions import Combinable

from .models import CustomUser


def get_current_user(
    user_id: typing.Union[
        BigAutoField[
            typing.Union[float, str, Combinable, None],
            int,
        ],
        typing.Any,
    ],
) -> typing.Union[CustomUser | None]:
    """Возвращает пользователя по его id, если он существует

    :param user_id: Id пользователя

    :return: Пользователя с указанным id, либо None, если пользователя с таким id нет
    """

    return CustomUser.objects.filter(pk=user_id).first()


def get_users_with_recipes() -> 'QuerySet[CustomUser]':
    """Возвращает пользователей вместе с рецептами и их количеством"""

    return CustomUser.objects.prefetch_related(
        'recipes',
    ).get_with_recipes_count()


def get_current_author(
    author_id: typing.Union[
        BigAutoField[
            typing.Union[float, str, Combinable, None],
            int,
        ],
        typing.Any,
    ],
    user_id: typing.Union[
        BigAutoField[
            typing.Union[float, str, Combinable, None],
            int,
        ],
        typing.Any,
    ],
) -> typing.Union[CustomUser | None]:
    """Возвращает автора с количеством рецептов и статусом подписки пользователя на этого автора

    :param author_id: Id автора
    :param user_id: Id пользователя

    :return: Автора с указанным id, либо None, если автора с таким id нет
    """

    return (
        CustomUser.objects
        .get_with_recipes_count()
        .get_with_subscription_status(
            subscriber_id=user_id,
        )
        .filter(
            pk=author_id,
        )
        .first()
    )
