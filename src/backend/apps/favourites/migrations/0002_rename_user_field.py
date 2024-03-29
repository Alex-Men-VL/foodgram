# Generated by Django 3.2.5 on 2022-08-04 08:58

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_rename_quantity_recipeingredient_amount'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('favourites', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favourite',
            old_name='author',
            new_name='user',
        ),
        migrations.AlterUniqueTogether(
            name='favourite',
            unique_together={('recipe', 'user')},
        ),
    ]
