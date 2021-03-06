# Generated by Django 3.2.5 on 2022-07-15 22:19

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ingredients', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created',
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    'modified',
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                (
                    'uuid',
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False
                    ),
                ),
                (
                    'title',
                    models.CharField(
                        db_index=True,
                        max_length=255,
                        unique=True,
                        verbose_name='Название',
                    ),
                ),
                (
                    'image',
                    models.ImageField(
                        upload_to='recipes/images', verbose_name='Картинка'
                    ),
                ),
                (
                    'description',
                    models.TextField(verbose_name='Текстовое описание'),
                ),
                (
                    'cooking_time',
                    models.PositiveSmallIntegerField(
                        help_text='В минутах.',
                        validators=[
                            django.core.validators.MinValueValidator(1)
                        ],
                        verbose_name='Время приготовления',
                    ),
                ),
                (
                    'author',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='recipes',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='Автор',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'quantity',
                    models.PositiveIntegerField(verbose_name='Количество'),
                ),
                (
                    'ingredient',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='recipe_ingredients',
                        to='ingredients.ingredient',
                        verbose_name='Ингредиент',
                    ),
                ),
                (
                    'recipe',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='recipe_ingredients',
                        to='recipes.recipe',
                        verbose_name='Рецепт',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Ингредиент в рецепте',
                'verbose_name_plural': 'Ингредиенты в рецепте',
                'unique_together': {('ingredient', 'recipe')},
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(
                related_name='recipes',
                through='recipes.RecipeIngredient',
                to='ingredients.Ingredient',
                verbose_name='Ингредиенты',
            ),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(
                related_name='recipes', to='tags.Tag', verbose_name='Теги'
            ),
        ),
    ]
