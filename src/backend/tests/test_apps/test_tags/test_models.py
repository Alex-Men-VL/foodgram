from django.db import IntegrityError
from django.test import TestCase

from apps.tags.models import Tag

from ...factories import TagFactory


class TagTest(TestCase):
    def setUp(self) -> None:
        self.tag: Tag = TagFactory()

    def test_tag_creation(self) -> None:
        """Проверка создания тега и корректность метода __str__."""

        self.assertTrue(isinstance(self.tag, Tag))
        self.assertEqual(str(self.tag), f'{self.tag.name}'.strip())

    def test_hex_code_validation(self) -> None:
        """Проверка валидации HEX-кода."""

        with self.assertRaises(IntegrityError):
            TagFactory.create(color='red')

    def test_name_color_unique_together(self) -> None:
        """Проверка совместной уникальности полей name и color."""

        with self.assertRaises(IntegrityError):
            TagFactory.create_batch(
                name='Завтра',
                color='#FFF000',
                size=2,
            )
