import typing

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.serializers import BaseSerializer

from django.db.models import QuerySet

from ..models import Recipe
from ..selectors import get_recipes_for_current_user
from .pagination import PageNumberLimitPagination
from .serializers import RecipeCreateSerializer
from .serializers import RecipeRetrieveSerializer


class RecipeViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet рецепта"""

    serializer_class = RecipeRetrieveSerializer
    pagination_class = PageNumberLimitPagination

    def get_queryset(self) -> 'QuerySet[Recipe]':
        current_user = self.request.user
        return get_recipes_for_current_user(
            user_id=current_user.pk,
        )

    def get_serializer_class(self) -> typing.Type[BaseSerializer]:
        if self.action == 'create':
            return RecipeCreateSerializer
        return self.serializer_class
