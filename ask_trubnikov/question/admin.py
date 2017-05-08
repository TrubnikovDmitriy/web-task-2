# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from models import *

admin.site.register(Profile)
admin.site.register(Tags)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(AnswerLikes)
admin.site.register(QuestionLikes)

# Register your models here.
