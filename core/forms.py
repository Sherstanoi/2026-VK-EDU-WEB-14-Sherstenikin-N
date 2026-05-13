from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(AuthenticationForm):
    """
    Наследуем стандартную форму аутентификации.
    Она проверяет логин/пароль и выдаёт ошибки.
    """
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class SignUpForm(UserCreationForm):
    """
    Форма регистрации. Добавляем поля email и nickname.
    """
    email = forms.EmailField(required=True, label='Email')
    nickname = forms.CharField(max_length=50, required=False, label='Ник')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Profile.objects.create(
                user=user,
                nickname=self.cleaned_data.get('nickname', '')
            )
        return user


class ProfileForm(forms.ModelForm):
    """
    Форма редактирования профиля.
    """
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = Profile
        fields = ('nickname', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=commit)
        if commit:
            user = profile.user
            user.email = self.cleaned_data['email']
            user.save()
        return profile