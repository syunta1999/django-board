# Generated by Django 3.2.9 on 2022-04-06 03:32

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_useractivatetokens'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='users',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
