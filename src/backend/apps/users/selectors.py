from django.db.models import QuerySet

from .models import CustomUser


def get_users_with_recipes() -> 'QuerySet[CustomUser]':
    """Возвращает пользователей вместе с рецептами и их количеством"""

    return CustomUser.objects.prefetch_related(
        'recipes',
    ).get_with_recipes_count()
