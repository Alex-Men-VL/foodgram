import typing

from django.db.models import BigAutoField
from django.db.models.expressions import Combinable

from .models import Favourite


def get_favourite(
    user_id: typing.Union[
        BigAutoField[
            typing.Union[float, str, Combinable, None],
            int,
        ],
        typing.Any,
    ],
    recipe_id: int,
) -> typing.Union[Favourite | None]:
    """Получение избранного

    :param user_id: Id пользователя
    :param recipe_id: Id рецепта
    """

    return (
        Favourite.objects
        .filter(
            user_id=user_id,
            recipe_id=recipe_id,
        )
        .first()
    )
