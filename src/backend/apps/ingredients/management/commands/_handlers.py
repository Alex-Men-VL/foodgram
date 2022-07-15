from abc import ABC
from abc import abstractmethod
import csv
import json
import os
from pathlib import Path
import typing
from urllib import parse
from urllib.request import urlopen

import pydantic

from django.core.management import CommandError

from ._models import Ingredient


class Handler(ABC):
    __supported_extensions: set = set()

    @abstractmethod
    def handle(self) -> typing.List[Ingredient]:
        """Обработка данных."""
        pass


class FileHandler(Handler):
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


class URLHandler(Handler):
    __supported_extensions = {'.json', '.csv'}

    def __init__(self, url: str) -> None:
        self.url = url
        self._extension = self._get_file_extension(url)
        self._check_url()

    def handle(self) -> typing.List[Ingredient]:
        """Обработка данных по URL."""

        payload = []
        if self._extension == '.json':
            payload = self._handle_json_from_url()
        elif self._extension == '.csv':
            payload = self._handle_csv_from_url()
        return payload

    def _check_url(self) -> None:
        """Проверка URL на корректность.

        :raise CommandError: Если URL не корректен или имеет неподдерживаемое расширение
        """

        parsed_url = parse.urlparse(parse.unquote(self.url))

        if not parsed_url.scheme:
            raise CommandError('Некорректный URL.')
        if not self._extension:
            raise CommandError('Файл не найден.')
        if self._extension not in self.__supported_extensions:
            raise CommandError('Не поддерживаемое расширение.')

    @staticmethod
    def _get_file_extension(url: str) -> str:
        """Парсит URL и возвращает расширение файла.

        :param url: URL путь файла
        """

        file_path = parse.urlparse(parse.unquote(url)).path
        _, file_extension = os.path.splitext(file_path)
        return file_extension

    def _handle_json_from_url(self) -> typing.List[Ingredient]:
        """Чтение и валидация json файла из URL."""

        with urlopen(self.url) as response:
            decoded_ingredients = json.loads(response.read().decode())
        ingredients = pydantic.parse_obj_as(
            typing.List[Ingredient],
            decoded_ingredients,
        )
        return ingredients

    def _handle_csv_from_url(self) -> typing.List[Ingredient]:
        """Чтение и валидация csv файла из URL."""

        ingredient_fields = list(Ingredient.schema()['properties'].keys())
        with urlopen(self.url) as response:
            lines = [line.decode() for line in response.readlines()]
            reader = csv.DictReader(lines, fieldnames=ingredient_fields)
            ingredients = pydantic.parse_obj_as(
                typing.List[Ingredient],
                list(reader),
            )
        return ingredients
