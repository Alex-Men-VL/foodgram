import typing

from drf_extra_fields.fields import Base64ImageField
from drf_writable_nested import NestedCreateMixin
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import Field

from apps.tags.api.serializers import TagSerializer
from apps.tags.models import Tag
from apps.users.api.serializers import UserSerializer

from . import RecipeIngredientFlatCreateSerializer
from . import RecipeIngredientFlatRetrieveSerializer
from . import ShortRecipeSerializer
from ...models import Recipe
from ...selectors import get_recipe_ingredients


class RecipeRetrieveSerializer(ShortRecipeSerializer):
    """Сериализатор получения рецепта"""

    tags = TagSerializer(
        read_only=True,
        many=True,
    )
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientFlatRetrieveSerializer(
        source='recipe_ingredients',
        many=True,
    )
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited_status',
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart_status',
    )

    class Meta(ShortRecipeSerializer.Meta):
        additional_fields = (
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'text',
        )
        fields = ShortRecipeSerializer.Meta.fields + additional_fields  # type: ignore

    def get_is_favorited_status(self, obj: Recipe) -> bool:
        """Возвращает статус добавлен ли текущий рецепт в избранное для текущего пользователя

        :param obj: Текущий рецепт
        """

        assert hasattr(
            obj,
            'is_favorited',
        ), 'У QuerySet не вызван метод get_with_favourite_status'

        return getattr(obj, 'is_favorited')

    def get_is_in_shopping_cart_status(self, obj: Recipe) -> bool:
        """Возвращает статус добавлен ли текущий рецепт в список покупок у текущего пользователя

        :param obj: Текущий рецепт
        """

        assert hasattr(
            obj,
            'is_in_shopping_cart',
        ), 'У QuerySet не вызван метод get_with_is_in_shopping_cart_status'

        return getattr(obj, 'is_in_shopping_cart')


class RecipeCreateSerializer(NestedCreateMixin, ShortRecipeSerializer):
    """Сериализатор создания рецепта"""

    image = Base64ImageField()
    tags: Field = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    ingredients = RecipeIngredientFlatCreateSerializer(
        source='recipe_ingredients',
        many=True,
    )

    class Meta(ShortRecipeSerializer.Meta):
        additional_fields = (
            'tags',
            'author',
            'ingredients',
            'text',
        )
        fields = ShortRecipeSerializer.Meta.fields + additional_fields  # type: ignore

    def update(
        self,
        instance: Recipe,
        validated_data: typing.Dict,
    ) -> Recipe:
        """Обновление рецепта"""

        ingredients_relations = self._extract_ingredients_relations(validated_data)

        # Update instance
        instance = super().update(
            instance,
            validated_data,
        )

        self.delete_recipe_ingredients(instance)
        if ingredients_relations:
            self.create_recipe_ingredients(instance, ingredients_relations)

        instance.refresh_from_db()
        return instance

    def _extract_ingredients_relations(
        self,
        validated_data: typing.Dict,
    ) -> typing.Union[typing.List[typing.Dict[str, int]] | None]:
        """Получение ингредиентов рецепта"""

        ingredients_field_name = 'ingredients'
        if ingredients_field := self.fields.get(ingredients_field_name):
            validated_data.pop(ingredients_field.source)

        return self.get_initial().get(ingredients_field_name)

    def delete_recipe_ingredients(
        self,
        recipe: Recipe,
    ) -> None:
        """Удаление рецептов

        :param recipe: Текущий рецепт
        """

        recipe_ingredients = get_recipe_ingredients(recipe)
        recipe_ingredients.delete()

    def create_recipe_ingredients(
        self,
        recipe: Recipe,
        ingredients_relations: typing.List[typing.Dict[str, int]],
    ) -> None:
        """Создание ингредиентов для текущего рецепта

        :param recipe: Текущий рецепт
        :param ingredients_relations: Ингредиенты
        """

        errors = []
        for ingredient in ingredients_relations:
            serializer = RecipeIngredientFlatCreateSerializer(
                data=ingredient,
            )
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save(
                    recipe=recipe,
                )
                errors.append({})
            except ValidationError as exc:
                errors.append(exc.detail)

        self._check_errors(errors)

    def _check_errors(self, errors: typing.List) -> None:
        """Вывод ошибок валидации

        :param errors: Список ошибок валидации
        """

        if any(errors):
            raise ValidationError({'ingredients': errors})
