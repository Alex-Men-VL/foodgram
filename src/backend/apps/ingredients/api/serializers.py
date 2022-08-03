from rest_framework import serializers

from ..models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов"""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class IngredientWithAmountSerializer(IngredientSerializer):
    """Сериализатор ингредиента вместе с количеством"""

    class Meta(IngredientSerializer.Meta):
        additional_fields = (
            'amount',
        )
        fields = IngredientSerializer.Meta.fields + additional_fields  # type: ignore
