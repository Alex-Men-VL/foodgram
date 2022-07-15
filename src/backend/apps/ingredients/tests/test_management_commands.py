from io import StringIO

from django.core.management import call_command
from django.core.management import CommandError
from django.test import TestCase

from ..models import Ingredient


class UploadIngredientsTest(TestCase):
    def call_command(self, *args: str, **kwargs: str) -> str:
        out: StringIO = StringIO()
        call_command(
            'upload_ingredients',
            *args,
            stdout=out,
            stderr=StringIO(),
            **kwargs,
        )
        return out.getvalue()

    def test_dry_run(self) -> None:
        with self.assertRaises(CommandError):
            out = self.call_command()
            self.assertEqual(out, 'Передайте путь к локальному файлу или URL.\n')

    def test_upload_from_json_file(self) -> None:
        self.assertEqual(Ingredient.objects.count(), 0)
        file_path: str = '/data/ingredients.json'

        out = self.call_command(
            '--file',
            file_path,
        )
        self.assertEqual(out, 'Ингредиенты успешно добавлены.\n')
        self.assertNotEqual(Ingredient.objects.count(), 0)

    def test_upload_from_csv_file(self) -> None:
        self.assertEqual(Ingredient.objects.count(), 0)
        file_path: str = '/data/ingredients.csv'

        out = self.call_command(
            '--file',
            file_path,
        )
        self.assertEqual(out, 'Ингредиенты успешно добавлены.\n')
        self.assertNotEqual(Ingredient.objects.count(), 0)

    def test_upload_from_json_url(self) -> None:
        self.assertEqual(Ingredient.objects.count(), 0)
        url: str = 'https://raw.githubusercontent.com/Alex-Men-VL/foodgram/main/data/ingredients.json'

        out = self.call_command(
            '--url',
            url,
        )
        self.assertEqual(out, 'Ингредиенты успешно добавлены.\n')
        self.assertNotEqual(Ingredient.objects.count(), 0)

    def test_upload_from_csv_url(self) -> None:
        self.assertEqual(Ingredient.objects.count(), 0)
        url: str = 'https://raw.githubusercontent.com/Alex-Men-VL/foodgram/main/data/ingredients.csv'

        out = self.call_command(
            '--url',
            url,
        )
        self.assertEqual(out, 'Ингредиенты успешно добавлены.\n')
        self.assertNotEqual(Ingredient.objects.count(), 0)
