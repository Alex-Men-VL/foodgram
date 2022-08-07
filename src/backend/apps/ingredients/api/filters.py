from django_filters import rest_framework as filters

from ..models import Ingredient


class IngredientNameFilter(filters.FilterSet):
    """Фильтрация по частичному вхождению в начале названия ингредиента"""

    name = filters.CharFilter(
        lookup_expr='icontains',
    )

    class Meta:
        models = Ingredient
        fields = (
            'name'
        )
