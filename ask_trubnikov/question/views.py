# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from question.forms import *
from question.models import *
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.utils import IntegrityError



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
        'post_list': post_list,
    })


def hot(request):
    hot_list = Question.objects.get_hot()[:75]
    post_list = listing(request, hot_list, 5)
    return render(request, 'hot.html', {
        'User': request.user,
        'post_list': post_list,
    })


def tag(request, tags):
    tag_list = Question.objects.by_tags(tags)
    return render(request, 'tag.html', {
        'tag': tags,
        'User': request.user,
        'post_list': listing(request, tag_list, 3)
    })


def question(request, question_id):
    quest = Question.objects.by_id(question_id)
    if request.POST:
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)

            # answer = Answer(
            #     question=quest,
            #     author=Profile.objects.all().get(user=request.user),
            #     text=answer_form.cleaned_data['text']
            #
            # ) Такой способ плохой?

            answer.question = quest
            answer.author = Profile.objects.all().get(user=request.user)
            answer.save()
            return redirect(
                '/question/' +
                str(answer.question_id) + '?page=0' +
                '#answer_id' + str(answer.id)
            )
    else:
        answer_form = AnswerForm()
    answer_list = Answer.objects.filter(question_id=question_id)
    post_list = listing(request, answer_list, 3)
    return render(request, 'single.html', {
        'User': request.user,
        'Question': quest,
        'Answers': post_list,
        'id': question_id,
        'answer_form': answer_form
    })


def signup(request):
    if request.POST:
        user_form = SignForm(
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid():
            user = User.objects.create_user(
                username=user_form.cleaned_data['username'],
                email=user_form.cleaned_data['email'],
                password=user_form.cleaned_data['password'],
                first_name=user_form.cleaned_data['first_name'],
                last_name=user_form.cleaned_data['last_name'],
            )
            profile = Profile(
                user=user,
                avatar=user_form.cleaned_data['avatar']
            )
            profile.save()
            return redirect('/')
    else:
        user_form = SignForm()
    return render(request, 'reg.html', {
        'User': request.user,
        'forms': user_form,
    })


@login_required()
def ask(request):
    if request.POST:
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            added_question = question_form.save(commit=False)
            added_question.author = Profile.objects.get(user=request.user)
            added_question.save()
            added_question.add_tag(question_form.cleaned_data['tags'])
            return redirect('/question/' + str(added_question.id))
    else:
        question_form = QuestionForm()
    return render(request, 'ask.html', {
        'User': request.user,
        'forms': question_form
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
                return redirect(request.POST.get('redirect_path'))
            else:
                # Авторизация не удалась
                auth_error = True
    else:
        # GET запрос
        form = LoginForm()
    return render(request, 'login.html', {
        'User': request.user,
        'forms': form,
        'auth_error': auth_error,
        'redirect_path': request.GET.get('next', '/')
        # Заполнение скрытого поля параметром GET-запроса
    })


@login_required()
def settings(request):
    is_success = False
    if request.POST:
        user_form = SettingForm(
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid():
            update_user = request.user

            new_pass = user_form.cleaned_data['password']
            if len(new_pass) != 0:
                update_user.set_password(new_pass)

            update_user.email = user_form.cleaned_data['email']
            update_user.first_name = user_form.cleaned_data['first_name']
            update_user.last_name = user_form.cleaned_data['last_name']
            update_user.save()

            update_profile = Profile.objects.get(user=update_user)
            new_avatar = user_form.cleaned_data['avatar']
            if new_avatar != None:
                update_profile.avatar.delete()
                update_profile.avatar = new_avatar
                update_profile.save()

            return redirect('/settings/?success=True')
    else:
        # Заполняем форму данными из БД
        user_form = SettingForm(instance=request.user)
        is_success = request.GET.get('success', default=False)
    return render(request, 'settings.html', {
        'User': request.user,
        'forms': user_form,
        'is_success': is_success
    })


@login_required()
def v_logout(request):
    logout(request)
    return redirect(request.META['HTTP_REFERER'])


@login_required
def vote(request):
    question_post = None
    if request.POST:
        likes_form = QuestionLikesForm(request.POST)
        question_post = Question.objects.get(id=request.POST['post_id'])
        author_like = Profile.objects.get(user=request.user)
        if likes_form.is_valid():
            new_like = likes_form.save(commit=False)
            new_like.author = author_like
            new_like.post = question_post
            try:
                # Проверяем является ли лайк/дизлайк абсолютно новым
                new_like.save()
            except IntegrityError:
                # Смена знака лайка
                old_like = QuestionLikes.objects.get(author=author_like, post=question_post)
                if old_like.sign != new_like.sign:
                    old_like.sign = new_like.sign
                    old_like.save()
                else:
                    # Не смог найти способа задизейблить кнопки так, чтобы
                    # сюда, в принципе, невозможно было попасть
                    print("Поытка двойного лайка от одного пользователя")

    # Получим перед выходом самый свежий рейтинг
    new_rate = question_post.update_rate()
    return JsonResponse({
        'new_rate': new_rate
    })


@login_required
def checked(request):
    if request.POST:
        answer = Answer.objects.get(id=request.POST['answer_id'])
        question_author = Profile.objects.get(id=request.POST['author_id'])
        # На всякий случай проверяем, что лайк от автора.
        # Потому что, если сильно захотеть, то можно
        # сделать не автором POST запрос
        if question_author.user == request.user:
            answer.checked = not answer.checked
            answer.save()
        else:
            print("Отметка не от автора!")

        return JsonResponse({
            'checked': answer.checked
        })
    else:
        # Если вдруг придет GET запрос, то пропускаем его
        return

# Create your views here.