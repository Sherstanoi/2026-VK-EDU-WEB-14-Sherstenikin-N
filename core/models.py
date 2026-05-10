from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    nickname = models.CharField(max_length=50, blank=True, verbose_name='Ник')

    def __str__(self):
        return f"Profile of {self.user.username}"