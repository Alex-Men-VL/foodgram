from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from django.contrib.auth import get_user_model

from ...recipes.api.serializers import ShortRecipeSerializer
from ..models import CustomUser as User

CustomUser = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    is_subscribed = serializers.SerializerMethodField(
        method_name='check_subscription',
        read_only=True,
    )

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def check_subscription(self, obj: User) -> bool:
        """Проверка подписки текущего пользователя на просматриваемого пользователя.

        :param obj: Пользователь, на которого проверяется подписка

        :return True: Если пользователь подписан на просматриваемого пользователя;
                False: Если пользователь не авторизован или просматривает свой профиль или не подписан.
        """

        assert hasattr(
            obj, 'is_subscribed',
        ), 'У QuerySet не вызван метод get_with_subscription_status'

        return obj.is_subscribed


class UserSubscriptionSerializer(UserSerializer):
    """Сериализатор пользователя с его рецептами."""

    recipes = ShortRecipeSerializer(
        many=True,
    )
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        additional_fields = (
            'recipes',
            'recipes_count',
        )
        fields = UserSerializer.Meta.fields + additional_fields  # type: ignore

    def get_recipes_count(self, obj: User) -> int:
        """Возвращает общее количество рецептов просматриваемого пользователя

        :param obj: Просматриваемый пользователь

        :return: Количество рецептов пользователя
        """

        assert hasattr(
            obj, 'recipes_count',
        ), 'У QuerySet не вызван метод get_with_recipes_count'

        return obj.recipes_count


class CurrentUserSerializer(UserSerializer):
    """Сериализатор текущего пользователя"""

    is_subscribed = serializers.BooleanField(default=False)
