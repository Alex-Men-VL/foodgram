import re
from io import StringIO

from django.core.management import call_command
from django.core.management import CommandError
from django.test import TestCase

from ..models import Ingredient


class UploadIngredientsTest(TestCase):
    def call_command(self, *args: str, **kwargs: str) -> str:
        """Вызов менеджмент команды."""

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
        """Тест вызовы команды без аргументов."""

        with self.assertRaises(CommandError):
            self.call_command()

    def _remove_ansi_escape_sequences(self, text: str) -> str:
        regex = r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])'
        ansi_escape = re.compile(regex)
        return ansi_escape.sub('', text)

    def test_upload_from_json_file(self) -> None:
        """Тест загрузки ингредиентов из локального JSON файла."""

        self.assertEqual(Ingredient.objects.count(), 0)
        file_path: str = '/data/ingredients.json'

        out = self.call_command(
            '--file',
            file_path,
        )
        out_without_color = self._remove_ansi_escape_sequences(out)
        self.assertEqual(out_without_color, 'Ингредиенты успешно добавлены.\n')
        self.assertNotEqual(Ingredient.objects.count(), 0)

    def test_upload_from_csv_file(self) -> None:
        """Тест загрузки ингредиентов из локального CSV файла."""

        self.assertEqual(Ingredient.objects.count(), 0)
        file_path: str = '/data/ingredients.csv'

        out = self.call_command(
            '--file',
            file_path,
        )
        out_without_color = self._remove_ansi_escape_sequences(out)
        self.assertEqual(out_without_color, 'Ингредиенты успешно добавлены.\n')
        self.assertNotEqual(Ingredient.objects.count(), 0)

    def test_upload_from_json_url(self) -> None:
        """Тест загрузки ингредиентов из JSON файла по URL."""

        self.assertEqual(Ingredient.objects.count(), 0)
        url: str = 'https://raw.githubusercontent.com/Alex-Men-VL/foodgram/main/data/ingredients.json'

        out = self.call_command(
            '--url',
            url,
        )
        out_without_color = self._remove_ansi_escape_sequences(out)
        self.assertEqual(out_without_color, 'Ингредиенты успешно добавлены.\n')
        self.assertNotEqual(Ingredient.objects.count(), 0)

    def test_upload_from_csv_url(self) -> None:
        """Тест загрузки ингредиентов из CSV файла по URL."""

        self.assertEqual(Ingredient.objects.count(), 0)
        url: str = 'https://raw.githubusercontent.com/Alex-Men-VL/foodgram/main/data/ingredients.csv'

        out = self.call_command(
            '--url',
            url,
        )
        out_without_color = self._remove_ansi_escape_sequences(out)
        self.assertEqual(out_without_color, 'Ингредиенты успешно добавлены.\n')
        self.assertNotEqual(Ingredient.objects.count(), 0)

    def test_file_not_found(self) -> None:
        """Тест передачи несуществующего файла."""

        self.assertEqual(Ingredient.objects.count(), 0)
        file_path: str = '/data/wrong_filename.csv'

        with self.assertRaises(CommandError):
            self.call_command(
                '--file',
                file_path,
            )

        self.assertEqual(Ingredient.objects.count(), 0)

    def test_unsupported_extension(self) -> None:
        """Тест передачи файла с неподдерживаемым расширением."""

        self.assertEqual(Ingredient.objects.count(), 0)
        file_path: str = '/data/ingredients.txt'

        with self.assertRaises(CommandError):
            self.call_command(
                '--file',
                file_path,
            )

        self.assertEqual(Ingredient.objects.count(), 0)

    def test_incorrect_url(self) -> None:
        """Тест передачи URL с некорректной схемой."""

        self.assertEqual(Ingredient.objects.count(), 0)
        url: str = 'raw.githubusercontent.com/Alex-Men-VL/foodgram/main/data/ingredients.csv'

        with self.assertRaises(CommandError):
            self.call_command(
                '--url',
                url,
            )

        self.assertEqual(Ingredient.objects.count(), 0)

    def test_url_file_not_found(self) -> None:
        """Тест передачи некорректного URL файла."""

        self.assertEqual(Ingredient.objects.count(), 0)
        url: str = 'https://raw.githubusercontent.com/Alex-Men-VL/foodgram/main/data/ingredients'

        with self.assertRaises(CommandError):
            self.call_command(
                '--url',
                url,
            )

        self.assertEqual(Ingredient.objects.count(), 0)

    def test_url_file_unsupported_extension(self) -> None:
        """Тест передачи URL с неподдерживаемым расширением файла."""

        self.assertEqual(Ingredient.objects.count(), 0)
        url: str = 'https://raw.githubusercontent.com/Alex-Men-VL/foodgram/main/data/ingredients.txt'

        with self.assertRaises(CommandError):
            self.call_command(
                '--url',
                url,
            )

        self.assertEqual(Ingredient.objects.count(), 0)
