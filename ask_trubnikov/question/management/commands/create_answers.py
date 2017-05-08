from django.core.management.base import BaseCommand
from question.models import Profile, Question, Answer
from faker import Faker
from random import *


class Command(BaseCommand):
    help = 'The single argument is count of created answers'

    def add_arguments(self, parser):
        parser.add_argument(
            'answers_count',
            nargs=1,
            type=int,
        )

    def handle(self, *args, **options):
        fake = Faker('it_IT')
        answers_count = options['answers_count'][0]
        author_list = Profile.objects.all().order_by('?')
        post_list = Question.objects.all().order_by('?')
        for _ in range(answers_count):
            a_rand = int(random() * (author_list.count() - 1))
            p_rand = int(random() * (post_list.count() - 1))
            answer = Answer(text=fake.text(max_nb_chars=200), author=author_list[a_rand],
                            question=post_list[p_rand])
            answer.save()
        self.stdout.write('Added ' + str(answers_count) + ' questions')