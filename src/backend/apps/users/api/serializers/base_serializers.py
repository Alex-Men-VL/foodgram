from rest_framework import serializers

from ...models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    is_subscribed: serializers.Field = serializers.SerializerMethodField(
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

    def check_subscription(self, obj: CustomUser) -> bool:
        """Проверка подписки текущего пользователя на просматриваемого пользователя.

        :param obj: Пользователь, на которого проверяется подписка

        :return True: Если пользователь подписан на просматриваемого пользователя;
                False: Если пользователь не авторизован или просматривает свой профиль или не подписан.
        """

        assert hasattr(
            obj,
            'is_subscribed',
        ), 'У QuerySet не вызван метод get_with_subscription_status'

        return obj.is_subscribed  # type: ignore
