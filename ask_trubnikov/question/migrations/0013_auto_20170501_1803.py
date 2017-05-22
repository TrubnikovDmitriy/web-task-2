# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-01 18:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0012_auto_20170501_1610'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='questionlikes',
            unique_together=set([('author', 'post')]),
        ),
        migrations.AlterModelTable(
            name='questionlikes',
            table='question_likes_for_post',
        ),
    ]