from model_bakery import baker

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from ..models import Tag


class TagTest(TestCase):

    def setUp(self) -> None:
        self.tag: Tag = baker.make(
            'tags.Tag',
            hex_code='#FFFFFF',
        )

    def test_ingredient_creation(self) -> None:
        """Проверка создания тега и корректность метода __str__."""

        self.assertTrue(isinstance(self.tag, Tag))
        self.assertEqual(str(self.tag), f'{self.tag.title}'.strip())

    def test_hex_code_validation(self) -> None:
        """Проверка валидации HEX-кода."""

        tag: Tag = baker.prepare(
            'tags.Tag',
            hex_code='#FFFF',
        )
        with self.assertRaises(ValidationError):
            tag.full_clean()

    def test_title_hex_code_unique_together(self) -> None:
        """Проверка совместной уникальности полей title и hex_code."""

        with self.assertRaises(IntegrityError):
            baker.make(
                'tags.Tag',
                title='Черный',
                hex_code='#000000',
                _quantity=2,
            )
