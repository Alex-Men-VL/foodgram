from collections.abc import Sequence
import typing

from factory import post_generation
from factory import SubFactory
from factory.django import DjangoModelFactory

from apps.carts.models import Cart

from .user_factory import UserFactory


class CartFactory(DjangoModelFactory):
    owner = SubFactory(UserFactory)

    class Meta:
        model = Cart

    @post_generation
    def recipes(
        self,
        create: bool,
        extracted: Sequence[typing.Any],
        **kwargs: typing.Dict,
    ) -> None:
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of recipes were passed in, use them
            for recipe in extracted:
                self.recipes.add(recipe)
