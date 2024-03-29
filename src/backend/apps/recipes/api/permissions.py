from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from ..models import Recipe


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Пермишен на уровне объекта, чтобы разрешить его редактирование только владельцам объекта."""

    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj: Recipe,
    ) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
