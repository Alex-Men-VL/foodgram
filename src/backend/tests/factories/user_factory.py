from collections.abc import Sequence
import typing

from djoser.conf import settings as djoser_settings
from factory import Faker
from factory import post_generation
from factory.django import DjangoModelFactory
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model

from apps.users.models import CustomUser

Token = djoser_settings.TOKEN_MODEL


class UserFactory(DjangoModelFactory):

    username = Faker('user_name')
    email = Faker('email')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    is_staff = False

    class Meta:
        model = get_user_model()
        django_get_or_create = ('username',)

    @post_generation
    def password(
        self,
        create: bool,
        extracted: Sequence[typing.Any],
        **kwargs: typing.Dict,
    ) -> None:
        password = (
            extracted
            if extracted
            else Faker(
                'password',
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={'locale': None})
        )
        self.set_password(password)


def login_user(client: APIClient, user: CustomUser) -> None:
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
