import csv
from io import StringIO
import json
import os
import re

from django.core.management import call_command
from django.core.management import CommandError
from django.test import TestCase

from apps.ingredients.models import Ingredient


class UploadIngredientsTest(TestCase):

    def setUp(self) -> None:
        self._create_correct_json_file()
        self._create_incorrect_json_file()
        self._create_correct_csv_file()
        self._create_file_with_unsupported_extension()

    def _create_correct_json_file(self) -> None:
        """Создание корректного json файла"""

        data = [
            {'name': 'варенье', 'measurement_unit': 'г'},
            {'name': 'пюре', 'measurement_unit': 'г'},
        ]
        self.correct_json_file = 'correct.json'

        with open(self.correct_json_file, 'w') as json_file:
            json.dump(data, json_file, indent=2)

    def _create_incorrect_json_file(self) -> None:
        """Создание некорректного json файла"""

        data = [
            {'title': 'варенье', 'unit': 'г'},
        ]
        self.incorrect_json_file = 'incorrect.json'

        with open(self.incorrect_json_file, 'w') as json_file:
            json.dump(data, json_file, indent=2)

    def _create_correct_csv_file(self) -> None:
        """Создание корректного csv файла"""

        data = ['варенье', 'г']
        self.correct_csv_file = 'correct.csv'

        with open(self.correct_csv_file, 'w', encoding='UTF8') as csv_file:
            writer = csv.writer(csv_file)

            writer.writerow(data)

    def _create_file_with_unsupported_extension(self) -> None:
        """Создание файла с неподдерживаемым расширением"""

        data = 'варенье, г'
        self.incorrect_file = 'file.txt'

        with open(self.incorrect_file, 'w') as f:
            f.write(data)

    def _remove_ansi_escape_sequences(self, text: str) -> str:
        regex = r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])'
        ansi_escape = re.compile(regex)
        return ansi_escape.sub('', text)

    def call_command(self, *args: str, **kwargs: str) -> str:
        """Вызов менеджмент команды"""

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

    def test_upload_from_json_file(self) -> None:
        """Тест загрузки ингредиентов из локального JSON файла."""

        self.assertEqual(Ingredient.objects.count(), 0)

        out = self.call_command(
            '--file',
            self.correct_json_file,
        )
        out_without_color = self._remove_ansi_escape_sequences(out)
        self.assertEqual(out_without_color, 'Ингредиенты успешно добавлены.\n')
        self.assertNotEqual(Ingredient.objects.count(), 0)

    def test_upload_from_csv_file(self) -> None:
        """Тест загрузки ингредиентов из локального CSV файла."""

        self.assertEqual(Ingredient.objects.count(), 0)

        out = self.call_command(
            '--file',
            self.correct_csv_file,
        )
        out_without_color = self._remove_ansi_escape_sequences(out)
        self.assertEqual(out_without_color, 'Ингредиенты успешно добавлены.\n')
        self.assertNotEqual(Ingredient.objects.count(), 0)

    def test_file_not_found(self) -> None:
        """Тест передачи несуществующего файла."""

        self.assertEqual(Ingredient.objects.count(), 0)
        file_path: str = 'wrong_filename.csv'

        with self.assertRaises(CommandError):
            self.call_command(
                '--file',
                file_path,
            )

        self.assertEqual(Ingredient.objects.count(), 0)

    def test_incorrect_file_format(self) -> None:
        """Тест передачи файла в некорректном формате"""

        self.assertEqual(Ingredient.objects.count(), 0)

        with self.assertRaises(CommandError):
            self.call_command(
                '--file',
                self.incorrect_json_file,
            )

        self.assertEqual(Ingredient.objects.count(), 0)

    def test_unsupported_extension(self) -> None:
        """Тест передачи файла с неподдерживаемым расширением."""

        self.assertEqual(Ingredient.objects.count(), 0)

        with self.assertRaises(CommandError):
            self.call_command(
                '--file',
                self.incorrect_file,
            )

        self.assertEqual(Ingredient.objects.count(), 0)

    def tearDown(self) -> None:
        os.remove(self.correct_json_file)
        os.remove(self.incorrect_json_file)
        os.remove(self.correct_csv_file)
        os.remove(self.incorrect_file)
