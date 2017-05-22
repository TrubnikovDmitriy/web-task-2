# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-01 02:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0008_auto_20170501_0219'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='seq',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='question.QuestionLikes'),
        ),
        migrations.AddField(
            model_name='answer',
            name='seq1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='question.Tags'),
        ),
    ]