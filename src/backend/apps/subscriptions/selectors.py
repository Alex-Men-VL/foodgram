from django.db.models.query import QuerySet

from ..users.models import CustomUser
from ..users.selectors import get_users_with_recipes


def get_user_subscriptions_authors(
    user: CustomUser,
) -> 'QuerySet[CustomUser]':
    """Возвращает список пользователей, на которых подписан пользователь

    :return: `QuerySet` объектов `CustomUser`, на которых подписан текущий пользователь
    """

    subscriptions = user.subscriptions.all()
    subscriptions_authors = subscriptions.values_list('author', flat=True)

    users_with_recipes = get_users_with_recipes()
    authors = (
        users_with_recipes
        .filter(pk__in=subscriptions_authors)
        .set_default_subscription_status(is_subscribed=True)  # type: ignore
    )
    return authors
