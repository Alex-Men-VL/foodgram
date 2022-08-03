from rest_framework import mixins
from rest_framework import viewsets

from ..models import Ingredient
from .serializers import IngredientSerializer


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """ViewSet ингредиента"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
