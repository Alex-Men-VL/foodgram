from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from apps.recipes.api.serializers import ShortRecipeSerializer

from . import UserSerializer
from ...models import CustomUser


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

    def get_recipes_count(self, obj: CustomUser) -> int:
        """Возвращает общее количество рецептов просматриваемого пользователя

        :param obj: Просматриваемый пользователь

        :return: Количество рецептов пользователя
        """

        assert hasattr(
            obj,
            'recipes_count',
        ), 'У QuerySet не вызван метод get_with_recipes_count'

        return obj.recipes_count  # type: ignore


class CurrentUserSerializer(UserSerializer):
    """Сериализатор текущего пользователя"""

    is_subscribed = serializers.BooleanField(default=False)
