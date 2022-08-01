import factory
from factory.django import DjangoModelFactory

from apps.favourites.models import Favourite

from .recipe_factory import RecipeFactory
from .user_factory import UserFactory


class FavouriteFactory(DjangoModelFactory):

    author = factory.SubFactory(UserFactory)
    recipe = factory.SubFactory(
        RecipeFactory,
        author=author,
    )

    class Meta:
        model = Favourite
