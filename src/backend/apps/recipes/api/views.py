from rest_framework import mixins
from rest_framework import viewsets

from django.db.models import QuerySet

from ..models import Recipe
from ..selectors import get_recipes_for_current_user
from .serializers import RecipeRetrieveSerializer


class RecipeViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet рецепта"""

    serializer_class = RecipeRetrieveSerializer

    def get_queryset(self) -> 'QuerySet[Recipe]':
        current_user = self.request.user
        return get_recipes_for_current_user(
            user_id=current_user.pk,
        )
