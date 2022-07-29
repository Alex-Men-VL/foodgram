from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from django.contrib.auth import get_user_model

from ...subscriptions.selectors import check_subscription_exist
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
        """Проверка подписки на текущего пользователя.

        :return True: Если пользователь подписан на просматриваемого пользователя;
                False: Если пользователь не авторизован или просматривает свой профиль или не подписан.
        """

        current_user = self.context.get('request').user  # type: ignore

        if current_user.is_anonymous or current_user == obj:
            return False

        return check_subscription_exist(
            author_uuid=obj.uuid,
            user_uuid=current_user.uuid,
        )
