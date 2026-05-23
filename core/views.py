# core/views.py
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import LoginForm, SignUpForm, ProfileForm
from .models import Profile


class LoginView(AuthLoginView):
    """
    Заменяет старый LoginView(TemplateView).
    Использует встроенную аутентификацию Django.
    """
    template_name = 'core/login-page.html'   # оставляем твоё имя шаблона
    form_class = LoginForm
    redirect_authenticated_user = True       # уже вошедших сразу редиректит

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # передаём img_url, если он нужен в шаблоне
        context['img_url'] = '/media/8e3de5c97eee1ca.webp'
        return context

    def get_success_url(self):
        """После успешного входа направляем на next или на главную."""
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        if next_url and url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        ):
            return next_url
        return reverse_lazy('questions:index')


class RegisterView(CreateView):
    """
    Заменяет старый RegisterView(TemplateView).
    Регистрация нового пользователя.
    """
    template_name = 'core/register-page.html'   # твой старый шаблон
    form_class = SignUpForm
    success_url = reverse_lazy('questions:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['img_url'] = '/media/8e3de5c97eee1ca.webp'
        return context

    def form_valid(self, form):
        """Сохраняем пользователя и сразу авторизуем."""
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class SettingsView(LoginRequiredMixin, UpdateView):
    """
    Заменяет старый SettingsView(TemplateView).
    Редактирование профиля. Доступно только авторизованным.
    """
    template_name = 'core/settings-page.html'   # твой старый шаблон
    model = Profile
    form_class = ProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['img_url'] = '/media/8e3de5c97eee1ca.webp'
        # Если нужно имя пользователя в шаблоне, оно уже есть в {{ user.username }}
        return context

    def get_object(self, queryset=None):
        """Возвращаем профиль текущего пользователя."""
        return self.request.user.profile

    def get_success_url(self):
        """После сохранения остаёмся на той же странице."""
        return reverse_lazy('core:settings')   # имя маршрута должно совпадать


class LogoutView(AuthLogoutView):
    """
    Выход. Перенаправляем на главную.
    """
    next_page = reverse_lazy('questions:index')