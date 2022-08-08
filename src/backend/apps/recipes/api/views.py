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

from ...carts.services import CartService
from ...favourites.services import FavouriteService
from ..models import Recipe
from ..selectors import get_recipes_for_current_user
from .filters import RecipeFilter
from .pagination import PageNumberLimitPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import RecipeCreateSerializer
from .serializers import RecipeRetrieveSerializer
from .serializers import ShortRecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet рецепта"""

    recipe_retrieve_serializer_class = RecipeRetrieveSerializer
    recipe_create_serializer_class = RecipeCreateSerializer
    favourite_serializer_class = FavouriteSerializer
    cart_recipe_serializer_class = ShortRecipeSerializer

    pagination_class = PageNumberLimitPagination
    permission_classes = (
        IsOwnerOrReadOnly,
    )
    filter_backends = (
        filters.DjangoFilterBackend,
    )
    filterset_class = RecipeFilter

    @action(methods=['get', 'delete'], detail=True, permission_classes=[IsAuthenticated])
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

    @action(detail=True, permission_classes=[IsAuthenticated])
    def shopping_cart(
        self,
        request: HttpRequest,
        pk: typing.Optional[int] = None,
    ) -> HttpResponse:
        """Эндпоинт для добавления рецепта в список покупок"""

        current_user = self.request.user
        current_recipe = get_object_or_404(
            self.get_queryset(),
            pk=pk,
        )

        service = CartService(
            user=current_user,
            recipe=current_recipe,
        )
        cart, added = service.add_recipe_to_shopping_cart()

        if not added:
            return Response(
                {
                    'errors': 'Рецепт уже добавлен в список покупок',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            current_recipe,
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @shopping_cart.mapping.delete
    def delete_recipe_from_shopping_cart(
        self,
        request: HttpRequest,
        pk: typing.Optional[int] = None,
    ) -> HttpResponse:
        """Эндпоинт для удаления рецепта из списка покупок"""

        current_user = self.request.user
        current_recipe = get_object_or_404(
            self.get_queryset(),
            pk=pk,
        )

        service = CartService(
            user=current_user,
            recipe=current_recipe,
        )
        deleted = service.remove_recipe_from_shopping_cart()

        if not deleted:
            return Response(
                {
                    'errors': 'Рецепт не был в списке покупок',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self) -> 'QuerySet[Recipe]':
        current_user = self.request.user
        return get_recipes_for_current_user(
            user_id=current_user.pk,
        )

    def get_serializer_class(self) -> typing.Type[BaseSerializer]:
        if self.action in {'create', 'update', 'partial_update'}:
            return self.recipe_create_serializer_class
        if self.action == 'favorite':
            return self.favourite_serializer_class
        if self.action == 'shopping_cart':
            return self.cart_recipe_serializer_class
        return self.recipe_retrieve_serializer_class
