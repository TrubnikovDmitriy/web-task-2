# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-01 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0010_auto_20170501_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='tag',
            field=models.CharField(max_length=7),
        ),
    ]
