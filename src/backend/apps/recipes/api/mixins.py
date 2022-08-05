import typing

from ..models import Recipe
from ..selectors import get_recipe_ingredients
from .serializers import RecipeIngredientFlatCreateSerializer


class RecipeUpdateMixin:
    """Миксин для обновления рецепта"""

    def update(
        self,
        instance: Recipe,
        validated_data: typing.Dict,
    ) -> Recipe:
        """Обновление рецепта"""

        ingredients_relations = self._extract_ingredients_relations(validated_data)

        # Update instance
        instance = super().update(  # type: ignore
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
        if ingredients_field := self.fields.get(ingredients_field_name):  # type: ignore
            validated_data.pop(ingredients_field.source)

        return self.get_initial().get(ingredients_field_name)  # type: ignore

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

        for ingredient in ingredients_relations:
            serializer = RecipeIngredientFlatCreateSerializer(
                data=ingredient,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(
                recipe=recipe,
            )
