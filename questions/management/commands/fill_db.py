import random
import gc
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from questions.models import Question, Answer, Tag, QuestionLike, AnswerLike

fake = Faker()

class Command(BaseCommand):
    help = 'Заполняет базу тестовыми данными. Использование: python manage.py fill_db <ratio>'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']
        self.stdout.write(f'Начинаем заполнение с ratio={ratio}')

        self.stdout.write('Создаю пользователей...')
        users = [User(username=fake.unique.user_name(), email=fake.email(), password='password') for _ in range(ratio)]
        User.objects.bulk_create(users, batch_size=2000)
        user_ids = list(User.objects.values_list('id', flat=True))
        self.stdout.write(f'Создано {len(user_ids)} пользователей')

        self.stdout.write('Создаю теги...')
        tags = []
        for i in range(ratio):
            try:
                name = fake.unique.word()[:42]
            except Exception:
                name = f'{fake.word()}_{i}'[:42]
            tags.append(Tag(name=name))
        Tag.objects.bulk_create(tags, batch_size=2000)
        tag_ids = list(Tag.objects.values_list('id', flat=True))
        self.stdout.write(f'Создано {len(tag_ids)} тегов')

        self.stdout.write('Создаю вопросы...')
        questions_batch = []
        total_q = ratio * 10
        for i in range(total_q):
            questions_batch.append(Question(
                title=fake.sentence()[:255],
                text=fake.text(max_nb_chars=4000),
                author_id=random.choice(user_ids)
            ))
            if len(questions_batch) >= 5000:
                Question.objects.bulk_create(questions_batch)
                self.stdout.write(f'  ...вопросов {i+1}/{total_q}')
                questions_batch.clear()
                gc.collect()
        if questions_batch:
            Question.objects.bulk_create(questions_batch)
        question_ids = list(Question.objects.values_list('id', flat=True))
        self.stdout.write(f'Создано {len(question_ids)} вопросов')

        self.stdout.write('Привязываю теги...')
        through = Question.tags.through
        q_tags_batch = []
        for qid in question_ids:
            for tid in random.sample(tag_ids, random.randint(1, 3)):
                q_tags_batch.append(through(question_id=qid, tag_id=tid))
                if len(q_tags_batch) >= 5000:
                    through.objects.bulk_create(q_tags_batch)
                    q_tags_batch.clear()
                    gc.collect()
        if q_tags_batch:
            through.objects.bulk_create(q_tags_batch)
        self.stdout.write('Теги привязаны')

        self.stdout.write('Создаю ответы (будет долго)...')
        answers_batch = []
        total_a = ratio * 100
        for i in range(total_a):
            answers_batch.append(Answer(
                question_id=random.choice(question_ids),
                text=fake.text(max_nb_chars=4000),
                author_id=random.choice(user_ids),
                is_correct=random.random() < 0.1
            ))
            if len(answers_batch) >= 5000:
                Answer.objects.bulk_create(answers_batch)
                self.stdout.write(f'  ...ответов {i+1}/{total_a}')
                answers_batch.clear()
                gc.collect()
        if answers_batch:
            Answer.objects.bulk_create(answers_batch)
            self.stdout.write(f'  ...ответов {total_a}/{total_a}')
        answer_ids = list(Answer.objects.values_list('id', flat=True))
        self.stdout.write(f'Создано {len(answer_ids)} ответов')

        self.stdout.write('Создаю лайки вопросов...')
        q_likes = set()
        q_likes_batch = []
        target_q_likes = ratio * 100
        while len(q_likes) < target_q_likes:
            uid = random.choice(user_ids)
            qid = random.choice(question_ids)
            if (uid, qid) not in q_likes:
                q_likes.add((uid, qid))
                q_likes_batch.append(QuestionLike(user_id=uid, question_id=qid))
                if len(q_likes_batch) >= 5000:
                    QuestionLike.objects.bulk_create(q_likes_batch)
                    self.stdout.write(f'  ...лайков вопросов {len(q_likes)}/{target_q_likes}')
                    q_likes_batch.clear()
                    gc.collect()
        if q_likes_batch:
            QuestionLike.objects.bulk_create(q_likes_batch)
            self.stdout.write(f'  ...лайков вопросов {len(q_likes)}/{target_q_likes}')
        self.stdout.write(f'Лайков вопросов: {QuestionLike.objects.count()}')

        self.stdout.write('Создаю лайки ответов...')
        a_likes = set()
        a_likes_batch = []
        target_a_likes = ratio * 100
        while len(a_likes) < target_a_likes:
            uid = random.choice(user_ids)
            aid = random.choice(answer_ids)
            if (uid, aid) not in a_likes:
                a_likes.add((uid, aid))
                a_likes_batch.append(AnswerLike(user_id=uid, answer_id=aid))
                if len(a_likes_batch) >= 5000:
                    AnswerLike.objects.bulk_create(a_likes_batch)
                    self.stdout.write(f'  ...лайков ответов {len(a_likes)}/{target_a_likes}')
                    a_likes_batch.clear()
                    gc.collect()
        if a_likes_batch:
            AnswerLike.objects.bulk_create(a_likes_batch)
            self.stdout.write(f'  ...лайков ответов {len(a_likes)}/{target_a_likes}')
        self.stdout.write(f'Лайков ответов: {AnswerLike.objects.count()}')

        self.stdout.write(self.style.SUCCESS(f'База полностью заполнена с ratio={ratio}'))