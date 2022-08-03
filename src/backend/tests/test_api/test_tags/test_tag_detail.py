from djet import assertions
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.tags.api.serializers import TagSerializer
from apps.tags.models import Tag

from ...factories import TagFactory


class TagViewSetDetailTest(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
    assertions.InstanceAssertionsMixin,
):
    def setUp(self) -> None:
        super().setUp()
        self.tag: Tag = TagFactory.create()
        self.base_url = 'api:tags-detail'

    def test_user_can_get_tag_detail(self) -> None:
        """Проверка успешного получения определенного тега"""

        response = self.client.get(
            reverse(
                self.base_url,
                args=[self.tag.pk],
            ),
        )

        self.assert_status_equal(response, status.HTTP_200_OK)
        self.assert_instance_exists(Tag, pk=self.tag.pk)

        tag = Tag.objects.get(pk=self.tag.pk)
        serializer = TagSerializer(
            tag,
        )

        self.assertEqual(response.data, serializer.data)

    def test_user_try_get_non_existent_tag_detail(self) -> None:
        """Проверка получения несуществующего тега"""

        incorrect_tag_id = 999
        response = self.client.get(
            reverse(
                self.base_url,
                args=[incorrect_tag_id],
            ),
        )

        self.assert_status_equal(response, status.HTTP_404_NOT_FOUND)
        self.assert_instance_does_not_exist(Tag, pk=incorrect_tag_id)
