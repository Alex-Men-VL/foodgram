from django_filters import rest_framework as filters

from apps.tags.models import Tag


class NumberInFilter(
    filters.BaseInFilter,
    filters.NumberFilter,
):
    pass


class RecipeFilter(filters.FilterSet):
    """Фильтрация для рецепта"""

    is_favorited = filters.BooleanFilter(
        label='Добавленные в избранное',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        label='Добавленные в список покупок',
    )
    author = NumberInFilter(
        field_name='author__id',
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        conjoined=True,
        queryset=Tag.objects.all(),
    )

    class Meta:
        fields = (
            'is_favorited',
            'is_in_shopping_cart',
            'author',
            'tags',
        )
