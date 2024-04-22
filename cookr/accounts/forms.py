from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import RadioSelect
from .models import Profile, UserPreferences, UserAllergies, UserAPIkeys


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class ProfileForm(forms.ModelForm):
    GOAL_CHOICES = [
        (0, 'Maintain weight'),
        (1, 'Lose weight'),
        (2, 'Gain weight'),
    ]

    goal = forms.ChoiceField(
        choices=GOAL_CHOICES,
        widget=RadioSelect,
        help_text="Select your fitness goal.",
        required=False
    )

    class Meta:
        model = Profile
        exclude = ('user', 'calories', 'protein', 'carbs', 'fat', 'sugar', 'sodium')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False


class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserPreferences
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False


class UserAllergiesForm(forms.ModelForm):
    class Meta:
        model = UserAllergies
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False


class UserAPIkeysForm(forms.ModelForm):
    class Meta:
        model = UserAPIkeys
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
