from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import Profile, UserPreferences, UserAllergies, UserAPIkeys

User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0


class UserPreferencesInline(admin.StackedInline):
    model = UserPreferences
    can_delete = False
    extra = 0


class UserAllergiesInline(admin.StackedInline):
    model = UserAllergies
    can_delete = False
    extra = 0


class UserAPIkeysInline(admin.StackedInline):
    model = UserAPIkeys
    can_delete = False
    extra = 0


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, UserPreferencesInline, UserAllergiesInline, UserAPIkeysInline)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
