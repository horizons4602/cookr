from django.shortcuts import redirect, render
from django.views.generic import View
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, ProfileForm, UserPreferencesForm, UserAllergiesForm, UserAPIkeysForm
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from recipes.views import edamam_api_call
from recipes.models import Recipe

# Constants for activity multipliers
ACTIVITY_MULTIPLIERS = {
    'sedentary': 1.2,
    'lightly_active': 1.375,
    'moderately_active': 1.55,
    'very_active': 1.725,
    'super_active': 1.9,
}

def calculate_calories(weight, height_in_inches, age, sex, activity_level):
    """
    Calculate daily calorie needs based on user information.

    Parameters:
    - weight: User's weight in kilograms
    - height_in_inches: User's height in inches
    - age: User's age in years
    - sex: User's sex (0 for male, 1 for female)
    - activity_level: User's activity level key as string

    Returns:
    - Calories: Daily calorie needs based on the Harris-Benedict equation
    """
    # Convert height from inches to centimeters
    height_cm = height_in_inches * 2.54

    if sex == 0:  # Male
        calories = (66 + (6.23 * weight) + (12.7 * height_cm) - (6.8 * age))
    else:  # Female
        calories = (655 + (4.35 * weight) + (4.7 * height_cm) - (4.7 * age))

    # Apply activity level multiplier
    multiplier = ACTIVITY_MULTIPLIERS.get(activity_level, 1.2)  # Default to sedentary if not found
    return calories * multiplier

@require_POST
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def index(request):
    return redirect("../demo/login")

class Register(FormView):
    template_name = 'accounts/register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class Account(LoginRequiredMixin, View):
    template_name = 'accounts/account.html'


    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        calories = calculate_calories(profile.weight, profile.height_in_inches, profile.age, profile.sex, profile.activity_level)

        # Round calories to nearest whole number
        calories = round(calories)

        # Calculate macronutrients based on rounded calorie value
        user_protein = round(calories / 4 / 4)  # Assuming protein and carbs are 4 calories per gram
        user_carbs = round(calories / 4 / 4)
        user_fat = round(calories / 9 / 9)      # Fat has approximately 9 calories per gram
        user_sugar = 36 if profile.sex == 0 else 25  # Added sugar limit in grams, standard dietary recommendation
        user_sodium = 2300  # Sodium limit in mg, standard dietary recommendation

        forms = {
            'profile_form': ProfileForm(instance=profile),
            'preferences_form': UserPreferencesForm(instance=request.user.userpreferences),
            'allergies_form': UserAllergiesForm(instance=request.user.userallergies),
            'apikeys_form': UserAPIkeysForm(instance=request.user.userapikeys),
        }

        context = {**forms, 'protein': user_protein, 'calories': calories, 'carbs': user_carbs, 'fat': user_fat, 'sugar': user_sugar, 'sodium': user_sodium}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        forms = {
            'profile_form': ProfileForm(request.POST, instance=request.user.profile),
            'preferences_form': UserPreferencesForm(request.POST, instance=request.user.userpreferences),
            'allergies_form': UserAllergiesForm(request.POST, instance=request.user.userallergies),
            'apikeys_form': UserAPIkeysForm(request.POST, instance=request.user.userapikeys),
        }

        if all(form.is_valid() for form in forms.values()):
            for form in forms.values():
                form.save()

            user = request.user
            recipe_instance, created = Recipe.objects.get_or_create(user=user)
            recipe_data = edamam_api_call(user)
            recipe_instance.add_recipes(recipe_data)

            return redirect('account')
        else:
            context = {**forms}
            return render(request, self.template_name, context)
