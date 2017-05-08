from django.core.management.base import BaseCommand
from question.models import Question, Answer, QuestionLikes, AnswerLikes


class Command(BaseCommand):
    help = 'Calculate rating of post by counting likes and dislikes'

    def handle(self, *args, **options):
        # Questions
        quest_list = Question.objects.all()
        likes_list = QuestionLikes.objects.all()
        self.stdout.write('Rate setting in questions is beginning...')
        for quest in quest_list:
            like = likes_list.filter(post=quest, sign=True).count()
            dislike = likes_list.filter(post=quest, sign=False).count()
            quest.rate = like - dislike
            quest.save()
        self.stdout.write('Rate setting in questions successfully completed!')

        # Answers
        answer_list = Answer.objects.all()
        likes_list = AnswerLikes.objects.all()
        self.stdout.write('Rate setting in answers is beginning...')
        for answer in answer_list:
            like = likes_list.filter(answer=answer, sign=True).count()
            dislike = likes_list.filter(answer=answer, sign=False).count()
            answer.rate = like - dislike
            answer.save()
        self.stdout.write('Rate setting in answers successfully completed!')
