from django.urls import path
from questions import views

app_name = 'questions'

urlpatterns = [
    path('', views.IndexView.as_view(), name = "index"),
    path('question/34', views.QuestionView.as_view(), name = "question"),
    path('tag/philosophy', views.TagView.as_view(), name = "tag"),
    path('newQuestion', views.NewQuestionView.as_view(), name = "new_question"),
]
