from factory import Faker
from factory.django import DjangoModelFactory

from apps.ingredients.models import Ingredient


class IngredientFactory(DjangoModelFactory):

    name = Faker('word')
    measurement_unit = Faker('random_element')

    class Meta:
        model = Ingredient
