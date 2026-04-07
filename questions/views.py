from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.paginator import Paginator

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
    
    if page_number.isdigit() and int(page_number) > 0:
        page_number = int(page_number)
    else:
        page_number = 1
    
    if page_number > paginator.num_pages:
        page_number = paginator.num_pages
    
    return paginator.page(page_number)


class IndexView(TemplateView):
    template_name='questions/main-page.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        page_obj = paginator(QUESTIONS, 3, self.request)
        context['questions'] = page_obj
        context['page_obj'] = page_obj
        return context
    

class TagView(TemplateView):
    template_name='questions/tag-page.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        page_obj = paginator(QUESTIONS, 3, self.request)
        context['questions'] = page_obj
        context['page_obj'] = page_obj
        return context
    
class QuestionView(TemplateView):
    template_name='questions/question-page.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['questions'] = QUESTION
        return context

class NewQuestionView(TemplateView):
    template_name='questions/new-question-page.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['questions'] = QUESTION
        return context