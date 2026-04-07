from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('login', views.LoginView.as_view(), name = "login"),
    path('register', views.RegisterView.as_view(), name = "register"),
    path('settings', views.SettingsView.as_view(), name = "settings"),
]
