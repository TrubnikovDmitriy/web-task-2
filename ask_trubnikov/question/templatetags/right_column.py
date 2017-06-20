# -*- coding: utf-8 -*-
from django import template
from question import models

register = template.Library()


@register.inclusion_tag('template_tag_box.html')
def show_tags_users():
    tags_list = models.Tags.objects.get_popular()[:16]
    best_user = models.Profile.objects.get_best()[:7]
    return {
        'tags_list': tags_list,
        'best_user': best_user
    }


# Чтобы не передавать в каждой вьювшке список лучших тегов и пользователей,
# выделим это в отдельный django.template.Library.inclusion_tag()
#
# Раньше все вьювшки передавали в шаблон best_user и tags_list:
# def index(request):
#     new_list = Question.objects.get_news()[:100]
#     post_list = listing(request, new_list, 5)
#     return render(request, 'index.html', {
#         'User': request.user,
#         'tags_list': Tags.objects.get_popular()[:16],
#         'best_user': Profile.objects.get_best()[:7],
#         'post_list': post_list,
#     })