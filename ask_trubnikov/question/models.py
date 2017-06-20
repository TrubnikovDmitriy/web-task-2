# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from faker import *


class ProfileManager(models.Manager):
    def get_old(self):
        return self.order_by('user__date_joined')

    def get_best(self):
        return self.annotate(activity=Count('answer')+Count('question')).order_by('-activity')


class QuestionManager(models.Manager):
    def get_news(self):
        return self.order_by('-created_at')

    def get_hot(self):
        return self.order_by('-rate')

    def by_tags(self, tag):
        return self.filter(tags__tag=tag)

    def by_id(self, id):
        try:
            return self.get(pk=id)
        except Question.DoesNotExist:
            return None


class TagsManager(models.Manager):
    def get_popular(self):
        return self.annotate(count_tag=Count('question')).order_by('-count_tag')


class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(
        upload_to='user_avatar/%Y',
        default='user_avatar/std_user_avatar.png',
    )
    objects = ProfileManager()

    def __unicode__(self):
        return self.user.username


class Tags(models.Model):
    tag = models.CharField(max_length=7, unique=True)
    objects = TagsManager()

    def __unicode__(self):
        return self.tag


class Question(models.Model):
    author = models.ForeignKey(Profile)
    title = models.CharField(max_length=50)
    text = models.TextField()
    tags = models.ManyToManyField(Tags)
    created_at = models.DateField(auto_now_add=True)
    rate = models.IntegerField(default=0)
    objects = QuestionManager()

    def count_answer(self):
        return Answer.objects.filter(question=self).count()

    def get_tags(self):
        return self.tags.all()[:3]

    def add_tag(self, tag_string):
        tag_list = tag_string.split("#")
        print tag_list
        all_tags = Tags.objects.all()
        for tag in tag_list:
            if len(tag) != 0:
                try:
                    self.tags.add(all_tags.get(tag=tag))
                except Tags.DoesNotExist:
                    new_tag = Tags(tag=tag)
                    new_tag.save()
                    self.tags.add(new_tag)

    def update_rate(self):
        all_likes = QuestionLikes.objects.filter(post=self)
        self.rate = all_likes.count() - 2 * all_likes.filter(sign=False).count()
        self.save()
        return self.rate


class QuestionLikes(models.Model):
    author = models.ForeignKey(Profile)
    post = models.ForeignKey(Question)
    sign = models.NullBooleanField()

    class Meta:
        unique_together = [('author', 'post')]


class Answer(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Profile)
    question = models.ForeignKey(Question)
    rate = models.IntegerField(default=0)
    checked = models.BooleanField(default=False)


class AnswerLikes(models.Model):
    author = models.ForeignKey(Profile)
    answer = models.ForeignKey(Answer)
    sign = models.NullBooleanField()

    class Meta:
        unique_together = [('author', 'answer')]

# Create your models here.