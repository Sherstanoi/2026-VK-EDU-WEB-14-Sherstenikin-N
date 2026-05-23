from django import forms
from .models import Question, Answer, Tag

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(max_length=255, required=False, help_text='Теги через запятую')

    class Meta:
        model = Question
        fields = ('title', 'text')

    def clean_tags(self):
        tags_str = self.cleaned_data['tags']
        tag_list = [t.strip() for t in tags_str.split(',') if t.strip()]
        return tag_list

    def save(self, user, commit=True):
        question = super().save(commit=False)
        question.author = user
        if commit:
            question.save()
            self.save_m2m()  
        tag_names = self.cleaned_data['tags']
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            question.tags.add(tag)
        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)