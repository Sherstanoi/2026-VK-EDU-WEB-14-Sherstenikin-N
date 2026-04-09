from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


QUESTIONS = [
    {
        'id':i,
        'title': 'aga',
        'text': "yea?"
    }
    for i in range(15)
]

QUESTION = [
    {
        'id':1,
        'title': 'aga',
        'text': "There is no great devine. You are free to choose, what is your own meaning of life. As long as you don`t make other people sad. BUT maybe there is something! Keep searching and surely you will find an answer.."
    }
    for i in range(2)
]

def paginator(items, per_page, request, page_param='page'):
    paginator = Paginator(items, per_page)
    page_number = request.GET.get(page_param, '1')
    
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    
    return page


class IndexView(TemplateView):
    template_name='questions/main-page.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        page_obj = paginator(QUESTIONS, 3, self.request)
        context['questions'] = page_obj
        context['page_obj'] = page_obj
        context['img_url'] = '/media/8e3de5c97eee1ca.webp'
        return context
    

class TagView(TemplateView):
    template_name='questions/tag-page.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        page_obj = paginator(QUESTIONS, 3, self.request)
        context['questions'] = page_obj
        context['page_obj'] = page_obj
        context['img_url'] = '/media/8e3de5c97eee1ca.webp'
        return context
    
class QuestionView(TemplateView):
    template_name='questions/question-page.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['questions'] = QUESTION
        context['img_url'] = '/media/8e3de5c97eee1ca.webp'
        return context

class NewQuestionView(TemplateView):
    template_name='questions/new-question-page.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['questions'] = QUESTION
        context['img_url'] = '/media/8e3de5c97eee1ca.webp'
        return context