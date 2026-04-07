from django.shortcuts import render
from django.views.generic import TemplateView

class LoginView(TemplateView):
    template_name='core/login-page.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        return context


class RegisterView(TemplateView):
    template_name='core/register-page.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        return context

 
class SettingsView(TemplateView):
    template_name='core/settings-page.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        return context