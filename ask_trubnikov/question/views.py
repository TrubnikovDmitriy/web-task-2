# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from question.models import *
from question.forms import *
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


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
        'User': request.user,
        'tags_list': Tags.objects.get_popular()[:16],
        'best_user': Profile.objects.get_best()[:7],
        'post_list': post_list,
    })


def hot(request):
    hot_list = Question.objects.get_hot()[:75]
    post_list = listing(request, hot_list, 5)
    return render(request, 'hot.html', {
        'User': request.user,
        'tags_list': Tags.objects.get_popular()[:16],
        'best_user': Profile.objects.get_best()[:7],
        'post_list': post_list,
    })


def tag(request, tags):
    tag_list = Question.objects.by_tags(tags)
    return render(request, 'tag.html', {
        'tag': tags,
        'User': request.user,
        'tags_list': Tags.objects.get_popular()[:16],
        'best_user': Profile.objects.get_best()[:7],
        'post_list': listing(request, tag_list, 3)
    })


def question(request, question_id):
    answer_list = Answer.objects.filter(question_id=question_id)
    post_list = listing(request, answer_list, 3)
    return render(request, 'single.html', {
        'User': request.user,
        'tags_list': Tags.objects.get_popular()[:16],
        'best_user': Profile.objects.get_best()[:7],
        'Question': Question.objects.by_id(question_id),
        'Answers': post_list,
        'id': question_id
    })


def v_login(request):
    auth_error = False
    if request.POST:
        # POST запрос
        form = LoginForm(request.POST)
        if form.is_valid():
            # Данные валидны
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if (user is not None) and user.is_active:
                # Авторизация удалась
                login(request, user)
                return redirect('/')
            else:
                # Авторизация не удалась
                auth_error = True
    else:
        # GET запрос
        form = LoginForm()
    return render(request, 'login.html', {
        'User': request.user,
        'tags_list': Tags.objects.get_popular()[:16],
        'best_user': Profile.objects.get_best()[:7],
        'forms': form,
        'auth_error': auth_error
    })


def signup(request):
    if request.POST:
        form = SignForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            # user = form.save() не хешируется пароль
            profile = Profile(
                user=user,
                avatar=form.cleaned_data['avatar']
            )
            profile.save()
            return redirect('/')
    else:
        form = SignForm()
    return render(request, 'reg.html', {
        'User': request.user,
        'tags_list': Tags.objects.get_popular()[:16],
        'best_user': Profile.objects.get_best()[:7],
        'forms': form,
    })


@login_required()
def ask(request):
    if request.POST:
        forms = QuestionForm(request.POST)
        if forms.is_valid():
            question = Question(
                author=Profile.objects.get(user=request.user),
                title=forms.cleaned_data['title'],
                text=forms.cleaned_data['text'],
                # tags.add(forms.cleaned_data['tags'])
            )
            question.save()
            print(forms.cleaned_data['tags'][0])
            new_tag = Tags.objects.get(tag=forms.cleaned_data['tags'][0])
            question.tags.add(new_tag)
            question.save()
            return redirect('/question/'+str(question.id))
    else:
        forms = QuestionForm()
    return render(request, 'ask.html', {
        'User': request.user,
        'tags_list': Tags.objects.get_popular()[:16],
        'best_user': Profile.objects.get_best()[:7],
        'forms': forms
    })


def v_logout(request):
    logout(request)
    return redirect(request.META['HTTP_REFERER'])

# Create your views here.
