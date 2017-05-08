from django.core.management.base import BaseCommand
from question.models import Profile, Tags, Question
from faker import Faker
from random import *


class Command(BaseCommand):
    help = 'The single argument is count of created questions'

    def add_arguments(self, parser):
        parser.add_argument(
            'questions_count',
            nargs=1,
            type=int,
        )

    def handle(self, *args, **options):
        fake = Faker('en_UK')
        size_a = Profile.objects.all().count()
        quest_count = options['questions_count'][0]
        for _ in range(quest_count):
            rand = random()
            rand = rand * (size_a - 1)
            r_author = Profile.objects.all()[rand: rand + 1]
            r_title = fake.text(max_nb_chars=50)
            r_text = fake.text(max_nb_chars=250)
            r_tags = Tags.objects.all().order_by('?')[:3]
            quest = Question(author=r_author[0], title=r_title, text=r_text, created_at=fake.date_time())
            quest.save()
            quest.tags.add(r_tags[0], r_tags[1], r_tags[2])
            quest.save()
        self.stdout.write('Added ' + str(quest_count) + ' questions')