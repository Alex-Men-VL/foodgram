import typing

from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from ...subscriptions.services import SubscriptionService
from ..models import CustomUser
from .serializers import UserSubscriptionSerializer


class UserViewSet(DjoserUserViewSet):
    """ViewSet пользователя."""

    queryset = CustomUser.objects.all()
    subscription_serializer_class = UserSubscriptionSerializer

    @action(methods=['get', 'delete'], detail=True)
    def subscribe(
        self,
        request: HttpRequest,
        id: typing.Optional[int] = None,
    ) -> HttpResponse:
        """Эндпоинт для добавления или удаления подписки на автора"""

        current_user = self.get_instance()
        authors = self.queryset.get_with_recipes().get_with_recipes_count()
        current_author = get_object_or_404(
            authors,
            pk=id,
        )

        service = SubscriptionService(
            author=current_author,
            subscriber=current_user,
        )

        if self.request.method == 'DELETE':
            deleted = service.dell_subscription()

            if not deleted:
                return Response(
                    {
                        'errors': 'Пользователь не был подписан на этого автора',
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(status=status.HTTP_204_NO_CONTENT)

        # Обработка метода `GET` - оформление подписки
        subscription, created = service.add_subscription()

        if not created:
            return Response(
                {
                    'errors': 'Подписка на этого автора уже существует',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_author.is_subscribed = True
        subscription_serializer = self.subscription_serializer_class(
            current_author,
            context={'request': request},
        )
        return Response(
            subscription_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def get_queryset(self) -> 'QuerySet[CustomUser]':
        current_user = self.get_instance()
        return (
            super()
            .get_queryset()
            .get_with_subscription_status(subscriber_id=current_user)
        )

    def get_permissions(self) -> typing.List[typing.Any]:
        if self.action == 'subscribe':
            permission_classes = [IsAuthenticated]
        else:
            return super().get_permissions()

        return [permission() for permission in permission_classes]
