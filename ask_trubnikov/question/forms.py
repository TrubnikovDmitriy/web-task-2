# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from question.models import *


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        max_length=30,
        min_length=2,
        label='Логин:',
        error_messages={'required': 'Пожалуйста введите логин'},
        widget=forms.TextInput(attrs={
            'class': 'form-control input-lg',
            'placeholder': 'Введите логин'
        })
    )
    password = forms.CharField(
        required=True,
        max_length=40,
        min_length=6,
        label='Пароль:',
        error_messages={'required': 'Пожалуйста введите пароль'},
        widget=forms.PasswordInput(attrs={
            'class': 'form-control input-lg',
            'placeholder': 'Введите пароль',
        })
    )


class SignForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]

    first_name = forms.CharField(
        required=True,
        max_length=30,
        min_length=2,
        error_messages={'required': 'Пожалуйста введите логин'},
        label='Имя:',
        widget=forms.TextInput(attrs={
            'class': 'form-control input-lg',
            'placeholder': 'Введите имя'
        })
    )
    last_name = forms.CharField(
        required=True,
        max_length=30,
        min_length=2,
        label='Фамилия:',
        widget=forms.TextInput(attrs={
            'class': 'form-control input-lg',
            'placeholder': 'Введите фамилию'
        })
    )
    email = forms.EmailField(
        required=True,
        max_length=35,
        label='Адрес email:',
        widget=forms.EmailInput(attrs={
            'class': 'form-control input-lg',
            'placeholder': 'Введите email'
        })
    )
    username = forms.CharField(
        required=True,
        max_length=25,
        label='Логин:',
        widget=forms.TextInput(attrs={
            'class': 'form-control input-lg',
            'placeholder': 'Введите логин'
        })
    )
    password = forms.CharField(
        required=True,
        max_length=40,
        label='Пароль:',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control input-lg',
            'placeholder': 'Введите пароль'
        })
    )
    password_confirm = forms.CharField(
        required=True,
        max_length=40,
        label='Подтверждение:',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control input-lg',
            'placeholder': 'Подтвердите пароль'
        })
    )
    avatar = forms.ImageField(
        required=False,
        label='Загрузить аватар:',
        widget=forms.FileInput()
    )


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    title = forms.CharField(
        required=True,
        label='Заголовок',
        max_length=70,
        widget=forms.TextInput(attrs={
            'class': 'form-control input-lg',
            'placeholder': 'Введите текст своего вопроса'
        })
    )
    text = forms.CharField(
        required=True,
        label='Текст:',
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'form-control ask-text input-lg',
            'placeholder': 'Опишите проблему',
            'rows': 5
        })
    )