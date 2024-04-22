from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import Profile, UserPreferences, UserAllergies, UserAPIkeys
from favorites.models import SavedOne, SavedTwo, SavedThree, SavedFour, SavedFive, SavedSix


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


class SavedOneInline(admin.StackedInline):
    model = SavedOne
    can_delete = False
    extra = 0


class SavedTwoInline(admin.StackedInline):
    model = SavedTwo
    can_delete = False
    extra = 0


class SavedThreeInline(admin.StackedInline):
    model = SavedThree
    can_delete = False
    extra = 0


class SavedFourInline(admin.StackedInline):
    model = SavedFour
    can_delete = False
    extra = 0


class SavedFiveInline(admin.StackedInline):
    model = SavedFive
    can_delete = False
    extra = 0


class SavedSixInline(admin.StackedInline):
    model = SavedSix
    can_delete = False
    extra = 0


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, UserPreferencesInline, UserAllergiesInline, UserAPIkeysInline, SavedOneInline, SavedTwoInline, SavedThreeInline, SavedFourInline, SavedFiveInline, SavedSixInline)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
