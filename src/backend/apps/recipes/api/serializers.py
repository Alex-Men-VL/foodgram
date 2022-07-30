from rest_framework import serializers

from ..models import Recipe


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Укороченный сериализатор рецепта."""

    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
