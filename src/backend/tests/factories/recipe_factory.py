from collections.abc import Sequence
import typing

from factory import Faker
from factory import post_generation
from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.django import ImageField

from apps.recipes.models import Recipe
from apps.recipes.models import RecipeIngredient

from .ingredients_factory import IngredientFactory
from .user_factory import UserFactory


class RecipeFactory(DjangoModelFactory):

    name = Faker('word')
    image = ImageField()
    text = Faker('paragraph')
    cooking_time = Faker('random_digit_not_null')
    author = SubFactory(UserFactory)

    class Meta:
        model = Recipe

    @post_generation
    def ingredients(
        self,
        create: bool,
        extracted: Sequence[typing.Any],
        **kwargs: typing.Dict,
    ) -> None:
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of ingredients were passed in, use them
            for ingredient in extracted:
                self.ingredients.add(ingredient)

    @post_generation
    def tags(
        self,
        create: bool,
        extracted: Sequence[typing.Any],
        **kwargs: typing.Dict,
    ) -> None:
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of tags were passed in, use them
            for tag in extracted:
                self.tags.add(tag)


class RecipeIngredientFactory(DjangoModelFactory):

    ingredient = SubFactory(IngredientFactory)
    amount = Faker('random_digit_not_null')

    class Meta:
        model = RecipeIngredient
