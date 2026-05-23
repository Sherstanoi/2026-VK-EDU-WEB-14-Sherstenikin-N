from django.urls import path
from questions import views

app_name = 'questions'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('hot/', views.HotView.as_view(), name='hot'),
    path('tag/<str:tag_name>/', views.TagView.as_view(), name='tag'),
    path('question/<int:pk>/', views.QuestionView.as_view(), name='question'),
    path('ask/', views.AskView.as_view(), name='new_question'),
    path('question/<int:pk>/answer/', views.add_answer, name='add_answer'),
]