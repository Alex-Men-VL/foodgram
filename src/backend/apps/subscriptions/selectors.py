from django.db.models.query import QuerySet

from ..users.models import CustomUser


def get_user_subscriptions_authors(
    user: CustomUser,
) -> 'QuerySet[CustomUser]':
    """Возвращает список пользователей, на которых подписан пользователь

    :return: `QuerySet` объектов `CustomUser`, на которых подписан текущий пользователь
    """

    subscriptions = user.subscriptions.all()
    subscriptions_authors = subscriptions.values_list('author', flat=True)

    authors = (
        CustomUser.objects.filter(pk__in=subscriptions_authors)
        .get_with_recipes()
        .get_with_recipes_count()
        .set_default_subscription_status(is_subscribed=True)
    )
    return authors
