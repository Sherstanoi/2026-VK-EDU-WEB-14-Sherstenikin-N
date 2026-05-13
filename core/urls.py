from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.RegisterView.as_view(), name='register'),   
    path('profile/', views.SettingsView.as_view(), name='settings'),  
    path('logout/', views.LogoutView.as_view(), name='logout'),
]