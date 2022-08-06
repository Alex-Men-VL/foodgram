from djet import assertions
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.recipes.api.serializers import RecipeRetrieveSerializer
from apps.recipes.models import Recipe
from apps.recipes.selectors import get_author_recipes_for_current_user
from apps.recipes.selectors import get_recipes_for_current_user
from apps.recipes.selectors import get_recipes_for_current_user_by_tags
from apps.tags.models import Tag
from apps.users.models import CustomUser

from ...factories import RecipeFactory
from ...factories import TagFactory
from ...factories import UserFactory


class RecipeViewSetListTest(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
):
    def setUp(self) -> None:
        super().setUp()
        self.user: CustomUser = UserFactory.create()
        self.recipe_author: CustomUser = UserFactory.create()

        self.breakfast_tag: Tag = TagFactory.create(slug='breakfast')
        self.lunch_tag: Tag = TagFactory.create(slug='lunch')
        self.dinner_tag: Tag = TagFactory.create(slug='dinner')

        self.first_recipe: Recipe = RecipeFactory.create(
            image=None,
            author=self.recipe_author,
            tags=(
                self.breakfast_tag,
                self.lunch_tag,
            ),
        )
        self.second_recipe: Recipe = RecipeFactory.create(
            image=None,
            tags=(
                self.breakfast_tag,
                self.lunch_tag,
                self.dinner_tag,
            ),
        )
        self.third_recipe: Recipe = RecipeFactory.create(
            image=None,
            tags=(
                self.dinner_tag,
            ),
        )

        self.base_url = 'api:recipes-list'

    def test_user_can_list_recipes(self) -> None:
        """Проверка успешного получения списка рецептов"""

        response = self.client.get(
            reverse(self.base_url),
        )

        self.assert_status_equal(response, status.HTTP_200_OK)

        recipes = get_recipes_for_current_user(self.user.pk)
        total_recipes_number = recipes.count()

        serializer = RecipeRetrieveSerializer(
            recipes,
            many=True,
        )
        response_recipes = response.json()['results']

        self.assertEqual(len(response_recipes), total_recipes_number)
        self.assertEqual(response_recipes, serializer.data)

    def test_user_can_filter_list_recipes_by_author(self) -> None:
        """Проверка успешной фильтрации списка рецептов по автору"""

        author_id = self.recipe_author.pk

        response = self.client.get(
            f'{reverse(self.base_url)}?author={author_id}',
        )

        self.assert_status_equal(response, status.HTTP_200_OK)

        recipes = get_author_recipes_for_current_user(
            author_id,
            self.user.pk,
        )
        total_recipes_number = recipes.count()

        serializer = RecipeRetrieveSerializer(
            recipes,
            many=True,
        )
        response_recipes = response.json()['results']

        self.assertEqual(len(response_recipes), total_recipes_number)
        self.assertEqual(response_recipes, serializer.data)

    def test_user_can_filter_list_recipes_by_tag_slug(self) -> None:
        """Проверка успешной фильтрации списка рецептов по тегу"""

        response = self.client.get(
            f'{reverse(self.base_url)}?tags={self.breakfast_tag.slug}',
        )

        self.assert_status_equal(response, status.HTTP_200_OK)

        recipes = get_recipes_for_current_user_by_tags(
            self.user.pk,
            [
                self.breakfast_tag,
            ],
        )
        total_recipes_number = recipes.count()

        serializer = RecipeRetrieveSerializer(
            recipes,
            many=True,
        )
        response_recipes = response.json()['results']

        self.assertEqual(len(response_recipes), total_recipes_number)
        self.assertEqual(response_recipes, serializer.data)
