# Generated by Django 3.2.5 on 2022-07-16 15:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
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
                    'author',
                    models.ForeignKey(
                        help_text='Тот, на кого подписался.',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='subscribers',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='Автор',
                    ),
                ),
                (
                    'subscriber',
                    models.ForeignKey(
                        help_text='Тот, кто подписался.',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='subscriptions',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='Подписчик',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Подписка на автора',
                'verbose_name_plural': 'Подписки на авторов',
                'unique_together': {('subscriber', 'author')},
            },
        ),
    ]
