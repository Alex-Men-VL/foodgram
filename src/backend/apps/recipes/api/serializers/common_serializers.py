from rest_framework import serializers

from apps.tags.api.serializers import TagSerializer
from apps.users.api.serializers import UserSerializer

from . import RecipeIngredientFlatSerializer
from . import ShortRecipeSerializer
from ...models import Recipe


class RecipeRetrieveSerializer(ShortRecipeSerializer):
    """Сериализатор получения рецепта"""

    tags = TagSerializer(
        read_only=True,
        many=True,
    )
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientFlatSerializer(
        source='recipe_ingredients',
        many=True,
    )
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited_status',
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart_status',
    )

    class Meta(ShortRecipeSerializer.Meta):
        additional_fields = (
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'text',
        )
        fields = ShortRecipeSerializer.Meta.fields + additional_fields  # type: ignore

    def get_is_favorited_status(self, obj: Recipe) -> bool:
        """Возвращает статус добавлен ли текущий рецепт в избранное для текущего пользователя

        :param obj: Текущий рецепт
        """

        assert hasattr(
            obj,
            'is_favorited',
        ), 'У QuerySet не вызван метод get_with_favourite_status'

        return getattr(obj, 'is_favorited')

    def get_is_in_shopping_cart_status(self, obj: Recipe) -> bool:
        """Возвращает статус добавлен ли текущий рецепт в список покупок у текущего пользователя

        :param obj: Текущий рецепт
        """

        assert hasattr(
            obj,
            'is_in_shopping_cart',
        ), 'У QuerySet не вызван метод get_with_is_in_shopping_cart_status'

        return getattr(obj, 'is_in_shopping_cart')
