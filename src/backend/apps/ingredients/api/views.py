from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework import viewsets

from ..models import Ingredient
from .filters import IngredientNameFilter
from .serializers import IngredientSerializer


class IngredientViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet ингредиента"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
    )
    filterset_class = IngredientNameFilter
