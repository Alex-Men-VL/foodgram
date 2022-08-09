import typing

from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from ...subscriptions.selectors import get_user_subscriptions_authors
from ...subscriptions.services import SubscriptionService
from ..models import CustomUser
from ..selectors import get_users_with_recipes
from .pagination import PageNumberLimitPagination
from .serializers import UserSubscriptionSerializer


class UserViewSet(DjoserUserViewSet):
    """ViewSet пользователя."""

    queryset = CustomUser.objects.all()
    subscription_serializer_class = UserSubscriptionSerializer
    pagination_class = PageNumberLimitPagination
    recipes_limit_query_param = 'recipes_limit'

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def subscriptions(
        self,
        request: HttpRequest,
    ) -> HttpResponse:
        """Эндпоинт для получения пользователей, на которых подписан текущий пользователь"""
        current_user = self.get_instance()
        queryset = get_user_subscriptions_authors(
            user=current_user,
        )

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(
            page,
            many=True,
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def subscribe(
        self,
        request: HttpRequest,
        id: typing.Optional[int] = None,
    ) -> HttpResponse:
        """Эндпоинт для добавления подписки на автора"""

        current_user = self.get_instance()
        users_with_recipes = get_users_with_recipes()
        current_author = get_object_or_404(
            users_with_recipes,
            pk=id,
        )

        service = SubscriptionService(
            author=current_author,
            subscriber=current_user,
        )
        subscription, created = service.add_subscription()

        if not created:
            return Response(
                {
                    'errors': 'Подписка на этого автора уже существует',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        setattr(current_author, 'is_subscribed', True)  # noqa: B010
        serializer = self.get_serializer(
            current_author,
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @subscribe.mapping.delete
    def unsubscribe(
        self,
        request: HttpRequest,
        id: typing.Optional[int] = None,
    ) -> HttpResponse:
        """Эндпоинт для отмены подписки на автора"""

        current_user = self.get_instance()
        users_with_recipes = get_users_with_recipes()
        current_author = get_object_or_404(
            users_with_recipes,
            pk=id,
        )

        service = SubscriptionService(
            author=current_author,
            subscriber=current_user,
        )
        deleted = service.dell_subscription()

        if not deleted:
            return Response(
                {
                    'errors': 'Пользователь не был подписан на этого автора',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self) -> 'QuerySet[CustomUser]':
        current_user = self.get_instance()
        return (
            super()
            .get_queryset()
            .get_with_subscription_status(subscriber_id=current_user)
        )

    def get_permissions(self) -> typing.List[typing.Any]:
        if self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        else:
            return super().get_permissions()

        return [permission() for permission in permission_classes]

    def get_serializer_class(self) -> typing.Type[Serializer] | typing.Any:
        if self.action in {'subscribe', 'subscriptions'}:
            return self.subscription_serializer_class
        return super().get_serializer_class()

    def get_serializer_context(self) -> typing.Dict[str, typing.Any]:
        context = super().get_serializer_context()

        recipes_limit = self.request.query_params.get(self.recipes_limit_query_param, -1)
        context[self.recipes_limit_query_param] = recipes_limit
        return context
