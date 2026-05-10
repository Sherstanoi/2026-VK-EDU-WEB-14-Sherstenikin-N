from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from .models import Question, Tag


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
    """
    Главная страница — список новых вопросов.
    """
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
    """
    Страница лучших вопросов (по количеству лайков).
    """
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
    """
    Список вопросов по конкретному тегу.
    """
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
    """
    Страница одного вопроса со списком ответов.
    """
    template_name = 'questions/question-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Основной вопрос с подсчётом лайков
        question = get_object_or_404(
            Question.objects.annotate(like_count=Count('question_likes'))
                             .prefetch_related('tags', 'answers__author'),
            pk=kwargs['pk']
        )
        # Ответы с подсчётом лайков
        answers = question.answers.annotate(
            like_count=Count('answer_likes')
        ).order_by('-is_correct', '-created_at')
        page_obj = paginate(answers, self.request, 3)

        context['question'] = question
        context['answers'] = page_obj
        context['page_obj'] = page_obj
        context['popular_tags'] = Tag.objects.order_by('?')[:9]
        context['img_url'] = '/media/8e3de5c97eee1ca.webp'
        return context


class NewQuestionView(TemplateView):
    """
    Страница создания нового вопроса (пока заглушка).
    """
    template_name = 'questions/new-question-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_tags'] = Tag.objects.order_by('?')[:9]
        context['img_url'] = '/media/8e3de5c97eee1ca.webp'
        return context