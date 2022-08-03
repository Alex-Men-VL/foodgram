from djet import assertions
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.tags.api.serializers import TagSerializer
from apps.tags.models import Tag

from ...factories import TagFactory


class TagViewSetListTest(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
):
    def setUp(self) -> None:
        super().setUp()
        self.total_tags_number = 3
        self.tags: Tag = TagFactory.create_batch(size=self.total_tags_number)
        self.base_url = 'api:tags-list'

    def test_user_can_list_tags(self) -> None:
        """Проверка успешного получения списка тегов"""

        response = self.client.get(
            reverse(self.base_url),
        )

        self.assert_status_equal(response, status.HTTP_200_OK)

        tags = Tag.objects.all()
        total_tags_number = tags.count()

        self.assertEqual(total_tags_number, self.total_tags_number)

        serializer = TagSerializer(
            tags,
            many=True,
        )

        self.assertEqual(len(response.json()), self.total_tags_number)
        self.assertEqual(response.json(), serializer.data)
