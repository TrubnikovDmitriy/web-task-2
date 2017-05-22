from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from question.models import Profile
from django.contrib.auth.models import User
from faker import Faker


class Command(BaseCommand):
    help = 'The single argument is count of created users (and profiles)'

    def add_arguments(self, parser):
        parser.add_argument(
            'users_count',
            nargs=1,
            type=int,
        )

    def handle(self, *args, **options):
        users_count = options['users_count'][0]
        fake_ru = Faker('ru_RU')
        fake_en = Faker('en_UK')

        i = 0
        while (i < users_count):
            try:
                if (fake_en.boolean()): #male
                    user = User.objects.create_user(
                        password='trubnikov',
                        is_superuser=False,
                        first_name=fake_ru.first_name_male(),
                        last_name=fake_ru.last_name_male(),
                        email=fake_en.email(),
                        is_staff=False,
                        is_active=True,
                        username=fake_en.user_name()
                    )
                else: #female
                    user = User.objects.create_user(
                        password='trubnikov',
                        is_superuser=False,
                        first_name=fake_ru.first_name_female(),
                        last_name=fake_ru.last_name_female(),
                        email=fake_en.email(),
                        is_staff=False,
                        is_active=True,
                        username=fake_en.user_name()
                    )
                profile = Profile(user=user)
                profile.save()
                i += 1
            except IntegrityError:
                self.stdout.write('Exception')
                continue
        self.stdout.write('Added ' + str(users_count) + ' users')