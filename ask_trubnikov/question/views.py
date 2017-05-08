# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from question.models import *


def listing(request, lists, step):
    page = request.GET.get('page', 1)
    pagination = Paginator(lists, step)
    try:
        page_list = pagination.page(page)
    except EmptyPage:
        page_list = pagination.page(pagination.num_pages)
    except PageNotAnInteger:
        page_list = pagination.page(1)
    return page_list


def index(request):
    new_list = Question.objects.get_news()[:100]
    post_list = listing(request, new_list, 5)
    return render(request, 'index.html', {
        'User': Profile.objects.get(user__username='Trubnikov'),
        'tags_list': Tags.objects.get_popular()[:16],
        'best_user': Profile.objects.get_best()[:7],
        'post_list': post_list,
    })


def hot(request):
    hot_list = Question.objects.get_hot()[:75]
    post_list = listing(request, hot_list, 5)
    return render(request, 'hot.html', {
        'User': Profile.objects.get(user__username='Trubnikov'),
        'tags_list': Tags.objects.get_popular()[:16],
        'best_user': Profile.objects.get_best()[:7],
        'post_list': post_list,
    })


def tag(request, tags):
    list = Question.objects.by_tags(tags)
    return render(request, 'tag.html', {
        'tag': tags,
        'User': Profile.objects.get(user__username='Trubnikov'),
        'tags_list': Tags.objects.get_popular()[:16],
        'best_user': Profile.objects.get_best()[:7],
        'post_list': listing(request, list, 3)
    })


def question(request, question_id):
    answer_list = Answer.objects.filter(question_id=question_id)
    post_list = listing(request, answer_list, 3)
    return render(request, 'single.html', {
        'User': Profile.objects.get(user__username='Trubnikov'),
        'tags_list': Tags.objects.get_popular()[:16],
        'best_user': Profile.objects.get_best()[:7],
        'Question': Question.objects.by_id(question_id),
        'Answers': post_list,
        'id': question_id
    })


def login(request):
    return render(request, 'login.html', {
        'User': Profile.objects.get(user__username='Trubnikov'),
        'tags_list': Tags.objects.get_popular()[:16],
        'best_user': Profile.objects.get_best()[:7],
    })


def signup(request):
    return render(request, 'reg.html', {
        'User': Profile.objects.get(user__username='Trubnikov'),
        'tags_list': Tags.objects.get_popular()[:16],
        'best_user': Profile.objects.get_best()[:7],
    })


def ask(request):
    return render(request, 'ask.html', {
        'User': Profile.objects.get(user__username='Trubnikov'),
        'tags_list': Tags.objects.get_popular()[:16],
        'best_user': Profile.objects.get_best()[:7],
    })


# Create your views here.
