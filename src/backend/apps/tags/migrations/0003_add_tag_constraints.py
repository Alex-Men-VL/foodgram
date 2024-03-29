# Generated by Django 3.2.5 on 2022-08-10 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_rename_tags_fields'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(fields=('name', 'color'), name='tags_tag_name_color_unique_together'),
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.CheckConstraint(check=models.Q(('name__len__gt', 0)), name='tags_tag_name_is_empty'),
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.CheckConstraint(check=models.Q(('color__startswith', '#'), ('color__len__in', (4, 7))), name='tags_tag_color_is_not_hex_code'),
        ),
    ]
