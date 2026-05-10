from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профиль'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_nickname')
    list_select_related = ('profile',)

    def get_nickname(self, instance):
        return instance.profile.nickname
    get_nickname.short_description = 'Ник'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)