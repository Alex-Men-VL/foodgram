import csv
import json
from pathlib import Path
import typing

import pydantic

from django.core.management import CommandError

from ._models import Ingredient


class FileHandler:
    __supported_extensions = {'.json', '.csv'}

    def __init__(self, file_path: str) -> None:
        self.file_path: Path = Path(file_path)
        self._extension = self.file_path.suffix
        self._check_file()

    def handle(self) -> typing.List[Ingredient]:
        """Обработка данных из локального файла."""

        payload = []
        if self._extension == '.json':
            payload = self._handle_json_file()
        elif self._extension == '.csv':
            payload = self._handle_csv_file()
        return payload

    def _check_file(self) -> None:
        """Проверка файла на существование и корректность.

        :raise CommandError: Когда файл не найден или указанный путь ведет не к файлу или файл имеет неподдерживаемое расширение
        """

        if not self.file_path.exists() or not self.file_path.is_file():
            raise CommandError('Файл не найден.')

        if self.file_path.suffix not in self.__supported_extensions:
            raise CommandError('Не поддерживаемое расширение.')

    def _handle_json_file(self) -> typing.List[Ingredient]:
        """Чтение и валидация локального json файла."""

        with open(self.file_path) as json_file:
            decoded_ingredients = json.load(json_file)
        ingredients = pydantic.parse_obj_as(
            typing.List[Ingredient],
            decoded_ingredients,
        )
        return ingredients

    def _handle_csv_file(self) -> typing.List[Ingredient]:
        """Чтение и валидация локального csv файла."""

        ingredient_fields = list(Ingredient.schema()['properties'].keys())
        with open(self.file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=ingredient_fields)
            ingredients = pydantic.parse_obj_as(
                typing.List[Ingredient],
                list(reader),
            )
        return ingredients
