from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, UserPreferences, UserAllergies, UserAPIkeys


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)


class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserPreferences
        exclude = ('user',)


class UserAllergiesForm(forms.ModelForm):
    class Meta:
        model = UserAllergies
        exclude = ('user',)


class UserAPIkeysForm(forms.ModelForm):
    class Meta:
        model = UserAPIkeys
        exclude = ('user',)