from django.contrib import admin
from .models import Question, Answer, Tag, QuestionLike, AnswerLike
from django.db import models

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    raw_id_fields = ('author',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'tag_list')
    list_filter = ('tags', 'created_at')
    search_fields = ('title', 'text')
    raw_id_fields = ('author',)
    inlines = (AnswerInline,)
    list_select_related = ('author',)
    list_prefetch_related = ('tags',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return ', '.join(t.name for t in obj.tags.all())
    tag_list.short_description = 'Теги'

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'question', 'author', 'is_correct', 'created_at')
    list_filter = ('is_correct', 'created_at')
    search_fields = ('text', 'question__title')
    raw_id_fields = ('question', 'author')
    list_select_related = ('question', 'author')

    def short_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    short_text.short_description = 'Ответ'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'question_count')
    search_fields = ('name',)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(q_count=models.Count('questions'))

    def question_count(self, obj):
        return obj.q_count
    question_count.short_description = 'Число вопросов'

@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'question')
    raw_id_fields = ('user', 'question')

@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'answer')
    raw_id_fields = ('user', 'answer')