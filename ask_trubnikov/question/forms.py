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
            'placeholder': 'Введите логин',
            'required': 'required',
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
            'required': 'required'
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
            'password',
            'password_confirm',
            'avatar'
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

    def clean(self):
        cleaned_data = super(SignForm, self).clean()
        pass_1 = cleaned_data['password']
        pass_2 = cleaned_data['password_confirm']

        if pass_1 != pass_2:
            error_message = u"Passwords do not match!"
            self._errors["password_confirm"] = self.error_class([error_message])
            del cleaned_data['password_confirm']

        if len(pass_1) < 6:
            error_message = u"Password is too short!"
            self._errors["password"] = self.error_class([error_message])
            del cleaned_data['password']

        return cleaned_data


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
    tags = forms.CharField(
        required=False,
        label="Теги:",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control input-lg',
            'placeholder': '#хештег'
        })
    )

    def clean(self):
        cleaned_data = super(QuestionForm, self).clean()
        tag_list = cleaned_data['tags'].split("#")
        error_message = ""
        for tag in tag_list:
            if len(tag) > 7:
                error_message += "Tag '" + tag + "' is too long"
                self._errors["tags"] = self.error_class([error_message])
                return cleaned_data
        return cleaned_data


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

    text = forms.CharField(
        required=True,
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'form-control answer-txt input-lg',
            'placeholder': 'Введите текст ответа',
            'rows': 3
        })
    )


class QuestionLikesForm(forms.ModelForm):
    class Meta:
        model = QuestionLikes
        fields = ['sign']


class SettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            # 'username',
            'password',
            'password_confirm',
            'avatar'
        ]

    first_name = forms.CharField(
        required=True,
        max_length=30,
        min_length=2,
        error_messages={'required': 'Это поле не может оставаться пустым'},
        label='Имя:',
        widget=forms.TextInput(attrs={
            'class': 'form-control input-lg',
        })
    )
    last_name = forms.CharField(
        required=True,
        max_length=30,
        min_length=2,
        error_messages={'required': 'Это поле не может оставаться пустым'},
        label='Фамилия:',
        widget=forms.TextInput(attrs={
            'class': 'form-control input-lg',
        })
    )
    email = forms.EmailField(
        required=True,
        error_messages={'required': 'Это поле не может оставаться пустым'},
        max_length=35,
        label='Адрес email:',
        widget=forms.EmailInput(attrs={
            'class': 'form-control input-lg',
        })
    )
    avatar = forms.ImageField(
        required=False,
        label='Изменить аватар:',
        widget=forms.FileInput()
    )
    password = forms.CharField(
        required=False,
        max_length=40,
        label='Пароль:',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control input-lg',
            'placeholder': 'Введите новый пароль'
        })
    )
    password_confirm = forms.CharField(
        required=False,
        max_length=40,
        label='Подтверждение:',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control input-lg',
            'placeholder': 'Чтобы не менять пароль, оставьте поля пустыми'
        })
    )

    def clean(self):
        cleaned_data = super(SettingForm, self).clean()
        pass_1 = cleaned_data['password']
        pass_2 = cleaned_data['password_confirm']

        if pass_1 != pass_2:
            error_message = u"Passwords do not match!"
            self._errors["password_confirm"] = self.error_class([error_message])
            del cleaned_data['password_confirm']

        if 0 < len(pass_1) < 6:
            error_message = u"Password is too short!"
            self._errors["password"] = self.error_class([error_message])
            del cleaned_data['password']

        return cleaned_data