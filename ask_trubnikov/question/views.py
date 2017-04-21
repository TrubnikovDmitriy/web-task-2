# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from fake_data import *


def listing(paginator, page):
    try:
        list = paginator.page(page)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        list = paginator.page(1)
    return list


def index(request):
    paginator = Paginator(many_post, 3)
    page = request.GET.get('page', 1)
    post_list = listing(paginator, page)
    return render(request, 'index.html',  {
        'User': User,
        'tags_list': tags_list,
        'best_user': best_user,
        'first_title': "новые вопросы",
        'second_title': "горячие вопросы",
        'post_list': post_list,
    })
def hot(request):
    page = request.GET.get('page')
    post_list = listing(Paginator(many_post, 2), page)
    return render(request, 'hot.html', {
        'User': User,
        'tags_list': tags_list,
        'best_user': best_user,
        'first_title': "горячие вопросы",
        'second_title': "новые вопросы",
        'post_list': post_list,
    })
def tag(request, tags):
    return render(request, 'tag.html', {
        'tag': tags,
        'User': User,
        'tags_list': tags_list,
        'best_user': best_user,
        'post_list': listing(Paginator(many_post, 5), request.GET.get('page', 1))
    })
def question(request, id):
    paginator = Paginator([Answer1, Answer2, Answer1], 2)
    page = request.GET.get('page')
    post_list = listing(paginator, page)
    return render(request, 'single.html', {
        'User': User,
        'tags_list': tags_list,
        'best_user': best_user,
        'Question': Post3,
        'Answers': post_list,
        'id': id
    })
def login(request):
    return render(request, 'login_error.html', {
        'User': User,
        'tags_list': tags_list,
        'best_user': best_user
    })
def signup(request):
    return render(request, 'reg.html', {
        'User': User,
        'tags_list': tags_list,
        'best_user': best_user
    })
def ask(request):
    return render(request, 'ask.html', {
        'User': User,
        'tags_list': tags_list,
        'best_user': best_user
    })

def base(request):
    return render(request, 'base.html', {
        'User': User,
        'tags_list': tags_list,
        'best_user': best_user,
    })


# Create your views here.
