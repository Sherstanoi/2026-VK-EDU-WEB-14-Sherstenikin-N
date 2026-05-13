from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.urls import reverse
from .models import Question, Tag
from .forms import QuestionForm, AnswerForm


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', '1')
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page


class IndexView(TemplateView):
    """Главная страница — список новых вопросов."""
    template_name = 'questions/main-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = Question.objects.new()
        page_obj = paginate(questions, self.request, 3)
        context['questions'] = page_obj
        context['page_obj'] = page_obj
        context['popular_tags'] = Tag.objects.order_by('?')[:9]
        context['img_url'] = '/media/8e3de5c97eee1ca.webp'
        return context


class HotView(TemplateView):
    """Страница лучших вопросов (по количеству лайков)."""
    template_name = 'questions/hot-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = Question.objects.best()
        page_obj = paginate(questions, self.request, 3)
        context['questions'] = page_obj
        context['page_obj'] = page_obj
        context['popular_tags'] = Tag.objects.order_by('?')[:9]
        context['img_url'] = '/media/8e3de5c97eee1ca.webp'
        return context


class TagView(TemplateView):
    """Список вопросов по конкретному тегу."""
    template_name = 'questions/tag-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(Tag, name=kwargs['tag_name'])
        questions = tag.questions.annotate(
            like_count=Count('question_likes')
        ).order_by('-created_at')
        page_obj = paginate(questions, self.request, 3)
        context['tag'] = tag
        context['questions'] = page_obj
        context['page_obj'] = page_obj
        context['popular_tags'] = Tag.objects.order_by('?')[:9]
        context['img_url'] = '/media/8e3de5c97eee1ca.webp'
        return context


class QuestionView(TemplateView):
    """Страница одного вопроса со списком ответов."""
    template_name = 'questions/question-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = get_object_or_404(
            Question.objects.annotate(like_count=Count('question_likes'))
                             .prefetch_related('tags', 'answers__author'),
            pk=kwargs['pk']
        )
        answers = question.answers.annotate(
            like_count=Count('answer_likes')
        ).order_by('-is_correct', '-created_at')
        page_obj = paginate(answers, self.request, 3)

        context['question'] = question
        context['answers'] = page_obj
        context['page_obj'] = page_obj
        context['popular_tags'] = Tag.objects.order_by('?')[:9]
        context['img_url'] = '/media/8e3de5c97eee1ca.webp'
        # Добавляем пустую форму ответа (для авторизованных)
        context['answer_form'] = AnswerForm()
        return context


class AskView(LoginRequiredMixin, CreateView):
    """
    Страница создания нового вопроса.
    Заменяет старый NewQuestionView (заглушку).
    """
    form_class = QuestionForm
    template_name = 'questions/new-question-page.html'

    def form_valid(self, form):
        # Передаём текущего пользователя в форму для сохранения
        question = form.save(user=self.request.user)
        return redirect(question.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_tags'] = Tag.objects.order_by('?')[:9]
        context['img_url'] = '/media/8e3de5c97eee1ca.webp'
        return context


def add_answer(request, pk):
    """Обработчик добавления ответа на вопрос."""
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST' and request.user.is_authenticated:
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            return redirect(
                f'{reverse("questions:question", kwargs={"pk": pk})}'
                f'?page=last#answer-{answer.pk}'
            )
    return redirect('questions:question', pk=pk)