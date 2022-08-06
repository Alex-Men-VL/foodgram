from collections import OrderedDict

from rest_framework import serializers
from rest_framework.fields import Field

from apps.ingredients.api.serializers import IngredientSerializer
from apps.ingredients.models import Ingredient

from ...models import Recipe
from ...models import RecipeIngredient


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Укороченный сериализатор рецепта"""

    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class RecipeIngredientFlatRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор получения ингредиента в рецепте"""

    ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredient
        fields = (
            'ingredient',
            'amount',
        )

    def to_representation(self, instance: RecipeIngredient) -> OrderedDict:
        representation = super().to_representation(instance)

        ingredient_representation = representation.pop('ingredient')
        for key in ingredient_representation:
            representation[key] = ingredient_representation[key]

        return representation


class RecipeIngredientFlatCreateSerializer(serializers.ModelSerializer):
    """Сериализатор добавления ингредиента в рецепт"""

    id: Field = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient',
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'amount',
        )
