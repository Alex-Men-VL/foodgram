import typing

from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from django.db.models import QuerySet
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from apps.favourites.api.serializers import FavouriteSerializer

from ...favourites.services import FavouriteService
from ..models import Recipe
from ..selectors import get_recipes_for_current_user
from .filters import RecipeFilter
from .pagination import PageNumberLimitPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import RecipeCreateSerializer
from .serializers import RecipeRetrieveSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet рецепта"""

    serializer_class = RecipeRetrieveSerializer
    pagination_class = PageNumberLimitPagination
    permission_classes = (
        IsOwnerOrReadOnly,
    )
    filter_backends = (
        filters.DjangoFilterBackend,
    )
    filterset_class = RecipeFilter
    favourite_serializer_class = FavouriteSerializer

    @action(methods=['get', 'delete'], detail=True)
    def favorite(
        self,
        request: HttpRequest,
        pk: typing.Optional[int] = None,
    ) -> HttpResponse:
        """Эндпоинт для добавления рецепта в избранное"""

        current_user = self.request.user
        current_recipe = get_object_or_404(
            self.get_queryset(),
            pk=pk,
        )

        service = FavouriteService(
            user=current_user,
            recipe=current_recipe,
        )

        if self.request.method == 'DELETE':
            deleted = service.remove_recipe_from_favorites()

            if not deleted:
                return Response(
                    {
                        'errors': 'Рецепт не был в списке избранного',
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(status=status.HTTP_204_NO_CONTENT)

        # Обработка метода `GET` - добавление рецепта в список избранного
        favourite, created = service.add_recipe_to_favorites()

        if not created:
            return Response(
                {
                    'errors': 'Рецепт уже добавлен в список избранного',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        favourite_serializer = self.favourite_serializer_class(
            favourite,
        )
        return Response(
            favourite_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def get_queryset(self) -> 'QuerySet[Recipe]':
        current_user = self.request.user
        return get_recipes_for_current_user(
            user_id=current_user.pk,
        )

    def get_serializer_class(self) -> typing.Type[BaseSerializer]:
        if self.action in {'create', 'update', 'partial_update'}:
            return RecipeCreateSerializer
        return self.serializer_class

    def get_permissions(self) -> typing.List[typing.Any]:
        if self.action in {'favorite'}:
            permission_classes = [IsAuthenticated]
        else:
            return super().get_permissions()

        return [permission() for permission in permission_classes]
