from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from question.models import Profile, Question, QuestionLikes
from faker import Faker
from random import *


class Command(BaseCommand):
    help = 'The single argument is count of created likes'

    def add_arguments(self, parser):
        parser.add_argument(
            'likes_count',
            nargs=1,
            type=int,
        )

    def handle(self, *args, **options):
        likes_count = options['likes_count'][0]
        fake = Faker('en_UK')
        author_list = Profile.objects.all()
        post_list = Question.objects.all()
        i = 0
        while (i < likes_count):
            a_rand = int(random() * author_list.count() - 1)
            p_rand = int(random() * post_list.count() - 1)
            like = QuestionLikes(author=author_list[a_rand], post=post_list[p_rand], sign=fake.boolean())
            try:
                like.save()
                i += 1
            except IntegrityError:
                self.stdout.write('Exception')
                continue
        self.stdout.write('Added ' + str(likes_count) + ' likes')