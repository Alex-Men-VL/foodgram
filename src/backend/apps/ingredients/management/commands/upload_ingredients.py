import typing

from pydantic import ValidationError

from django.apps import apps
from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.core.management.base import CommandParser
from django.db import transaction

from ._handlers import FileHandler
from ._handlers import Handler
from ._handlers import URLHandler
from ._models import Ingredient


class Command(BaseCommand):
    help = 'Добавить ингредиенты из файлы.'

    __supported_extensions = {'.json', '.csv'}

    def handle(self, *args: str, **options: str) -> None:
        handler: Handler

        if file_path := options.get('file'):
            handler = FileHandler(file_path)
        elif file_url := options.get('url'):
            handler = URLHandler(file_url)
        else:
            raise CommandError('Передайте путь к локальному файлу или URL.')

        try:
            ingredients = handler.handle()
        except ValidationError:
            raise CommandError('Не корректный формат файла.')

        self._save_ingredients(ingredients)
        self.stdout.write('Ингредиенты успешно добавлены.')

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--file',
            help='Путь к локальному файлу с ингредиентами.',
            type=str,
        )
        parser.add_argument(
            '--url',
            help='URl адрес файла с ингредиентами.',
            type=str,
        )

    @staticmethod
    @transaction.atomic
    def _save_ingredients(ingredients: typing.List[Ingredient]) -> None:
        """Сохранение ингредиентов в базу данных.

        :param ingredients: Список ингредиентов
        """

        ingredient_model = apps.get_model('ingredients', 'Ingredient')
        ingredient_model.objects.bulk_create(
            [ingredient_model(**ingredient.dict()) for ingredient in ingredients],
            ignore_conflicts=True,
        )
