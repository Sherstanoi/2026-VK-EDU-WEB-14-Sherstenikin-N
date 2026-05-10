from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

class Tag(models.Model):
    name = models.CharField(max_length=42, unique=True, verbose_name='Имя тэга')

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def best(self):
        return self.select_related('author').prefetch_related('tags').annotate(
            like_count=Count('question_likes'),
            answer_count=Count('answers')
        ).order_by('-like_count')

    def new(self):
        return self.select_related('author').prefetch_related('tags').annotate(
            like_count=Count('question_likes'),
            answer_count=Count('answers')
        ).order_by('-created_at')


class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name='Вопрос')
    text = models.TextField(max_length=4096, verbose_name='Текст вопроса')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions', verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    tags = models.ManyToManyField(Tag, related_name='questions', blank=True, verbose_name='Тэги')

    objects = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='Вопрос')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers', verbose_name='Автор')
    text = models.TextField(max_length=4096, verbose_name='Текст ответа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ли ответ')

    def __str__(self):
        return f"Answer to '{self.question.title}' by {self.author.username}"


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_questions', verbose_name='Пользователь')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_likes', verbose_name='Вопрос')

    class Meta:
        unique_together = ('user', 'question') 
        verbose_name = 'Лайк вопроса'
        verbose_name_plural = 'Лайки вопросов'

    def __str__(self):
        return f"{self.user.username} likes {self.question.title}"


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_answers', verbose_name='Пользователь')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_likes', verbose_name='Ответ')

    class Meta:
        unique_together = ('user', 'answer')
        verbose_name = 'Лайк ответа'
        verbose_name_plural = 'Лайки ответов'

    def __str__(self):
        return f"{self.user.username} likes answer #{self.answer.pk}"