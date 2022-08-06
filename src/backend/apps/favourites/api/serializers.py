from collections import OrderedDict

from rest_framework import serializers

from apps.recipes.api.serializers import ShortRecipeSerializer

from ..models import Favourite


class FavouriteSerializer(serializers.ModelSerializer):
    """Сериализатор избранного рецепта"""

    recipe = ShortRecipeSerializer()
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Favourite
        fields = (
            'recipe',
            'author',
        )

    def to_representation(self, instance: Favourite) -> OrderedDict:
        representation = super().to_representation(instance)

        ingredient_representation = representation.pop('recipe')
        for key in ingredient_representation:
            representation[key] = ingredient_representation[key]

        return representation
