from rest_framework import mixins
from rest_framework import viewsets

from ..models import Tag
from .serializers import TagSerializer


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """ViewSet тега"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
