from django.core.management.base import BaseCommand
from django.core.cache import cache
from question.models import Tags, Profile


class Command(BaseCommand):

    def handle(self, *args, **options):
        cache.clear()
        tags_list = Tags.objects.get_popular()[:16]
        best_users = Profile.objects.get_best()[:7]
        cache.set('update_tags', tags_list, 350)
        cache.set('update_users', best_users, 350)
        print("The cache has been successfully updated!")
        return
