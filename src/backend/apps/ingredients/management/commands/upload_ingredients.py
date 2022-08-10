import typing

from pydantic import ValidationError

from django.apps import apps
from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.core.management.base import CommandParser
from django.db import transaction

from ._handlers import FileHandler
from ._models import Ingredient


class Command(BaseCommand):
    help = 'Добавить ингредиенты из файлы.'

    __supported_extensions = {'.json', '.csv'}

    def handle(self, *args: str, **options: str) -> None:
        file_path = options.get('file', '')
        handler = FileHandler(file_path)

        try:
            ingredients = handler.handle()
        except ValidationError:
            raise CommandError('Не корректный формат файла.')

        self._save_ingredients(ingredients)
        self.stdout.write(self.style.SUCCESS('Ингредиенты успешно добавлены.'))

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--file',
            help='Путь к локальному файлу с ингредиентами.',
            type=str,
            required=True,
        )

    @staticmethod
    @transaction.atomic
    def _save_ingredients(ingredients: typing.List[Ingredient]) -> None:
        """Сохранение ингредиентов в базу данных.

        :param ingredients: Список ингредиентов
        """

        ingredient_model = apps.get_model('ingredients', 'Ingredient')
        ingredient_model.objects.bulk_create(
            [
                ingredient_model(**ingredient.dict())
                for ingredient in ingredients
            ],
            ignore_conflicts=True,
        )
