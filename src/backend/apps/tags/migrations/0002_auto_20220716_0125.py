# Generated by Django 3.2.5 on 2022-07-15 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='hex_code',
            new_name='color',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='title',
            new_name='name',
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together={('name', 'color')},
        ),
    ]