# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from django.contrib.auth.models import User # Берем готовую модель Юзера (по тз)


# class QuestionManager(models.Manager):
#     def get_newest(self):


class Profile(models.Model): # Расширяем класс Юзер
    user = models.OneToOneField(User)

class Question(models.Model):
    title = models.CharField(max_length=12)
    text  = models.TextField()
    author = models.ForeignKey(User)
    created_at = models.DateField(auto_now_add=True)

class Answer(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User)
    question = models.ForeignKey(Question)

# Create your models here.
