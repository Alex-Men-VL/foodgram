# Generated by Django 3.2.5 on 2022-08-02 16:07

import apps.users.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', apps.users.models.CustomUserManager()),
            ],
        ),
    ]
