from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import SignUpForm, ProfileForm, UserPreferencesForm, UserAllergiesForm, UserAPIkeysForm
from .views import calculate_calories, ACTIVITY_MULTIPLIERS
from unittest.mock import patch
from django.forms.models import model_to_dict
from django.http import HttpResponse


class AccountTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_calculate_calories_male(self):
        weight = 70
        height_in_inches = 70
        age = 25
        sex = 0  # Male
        activity_level = 'moderately_active'
        expected_calories = (66 + (6.23 * weight) + (12.7 * height_in_inches * 2.54) - (6.8 * age))
        expected_calories *= ACTIVITY_MULTIPLIERS[activity_level]
        calories = calculate_calories(weight, height_in_inches, age, sex, activity_level)
        self.assertEqual(round(calories), round(expected_calories))

    def test_calculate_calories_female(self):
        weight = 60
        height_in_inches = 65
        age = 30
        sex = 1  # Female
        activity_level = 'lightly_active'
        expected_calories = (655 + (4.35 * weight) + (4.7 * height_in_inches * 2.54) - (4.7 * age))
        expected_calories *= ACTIVITY_MULTIPLIERS[activity_level]
        calories = calculate_calories(weight, height_in_inches, age, sex, activity_level)
        self.assertEqual(round(calories), round(expected_calories))

    def test_logout_view(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertTrue(response.url.startswith(reverse('login')))  # Redirect to login

    def test_index_view_redirects(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)  # Check if there is a redirect

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_view_post_valid(self):
        form_data = {'username': 'newuser', 'password': 'newpassword123', 'email': 'newuser@example.com'}
        with patch.object(SignUpForm, 'is_valid', return_value=True), \
             patch.object(SignUpForm, 'save', return_value=None):
            response = self.client.post(reverse('register'), form_data)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith(reverse('login')))

    def test_account_view_post_valid(self):
        form_data = {'profile_form': model_to_dict(self.user.profile),
                     'preferences_form': model_to_dict(self.user.userpreferences),
                     'allergies_form': model_to_dict(self.user.userallergies),
                     'apikeys_form': model_to_dict(self.user.userapikeys)}
        with patch.object(ProfileForm, 'is_valid', return_value=True), \
             patch.object(UserPreferencesForm, 'is_valid', return_value=True), \
             patch.object(UserAllergiesForm, 'is_valid', return_value=True), \
             patch.object(UserAPIkeysForm, 'is_valid', return_value=True), \
             patch.object(ProfileForm, 'save', return_value=None), \
             patch.object(UserPreferencesForm, 'save', return_value=None), \
             patch.object(UserAllergiesForm, 'save', return_value=None), \
             patch.object(UserAPIkeysForm, 'save', return_value=None):
            response = self.client.post(reverse('account'), form_data)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith(reverse('account')))
