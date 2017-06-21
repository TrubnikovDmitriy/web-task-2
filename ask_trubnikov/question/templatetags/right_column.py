# -*- coding: utf-8 -*-
from django import template
from django.core.cache import cache
from question.models import QuestionLikes, Profile
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()


@register.inclusion_tag('template_tag_box.html')
def show_tags_users():
    # tags_list = models.Tags.objects.get_popular()[:16]
    # best_user = models.Profile.objects.get_best()[:7]

    # Кеш обновлять будем извне через сron и managment.commands, каждые 5 минут
    tags_list = cache.get('update_tags', None)
    best_user = cache.get('update_users', None)

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


@register.filter(name='disable')
def disable(question, user):
    profile = Profile.objects.get(user=user)
    try:
        return QuestionLikes.objects.get(post=question, author=profile).sign
    except ObjectDoesNotExist:
        return None
