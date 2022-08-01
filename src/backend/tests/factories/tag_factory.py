from factory import Faker
from factory import Sequence
from factory.django import DjangoModelFactory

from apps.tags.models import Tag


class TagFactory(DjangoModelFactory):

    name = Faker('word')
    color = Sequence(lambda n: '#%06d' % n)

    class Meta:
        model = Tag
