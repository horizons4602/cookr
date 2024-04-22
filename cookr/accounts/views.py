from django.shortcuts import redirect, render
from django.views.generic import View
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, ProfileForm, UserPreferencesForm, UserAllergiesForm, UserAPIkeysForm
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse


def calculate_calories(weight, height, age, sex, activity_level):
    """
    Calculate daily calorie needs based on user information.

    Parameters:
    - weight: User's weight in kilograms
    - height: User's height in centimeters
    - age: User's age in years
    - sex: User's sex (either 'Male' or 'Female')
    - activity_level: User's activity level (a float value)

    Returns:
    - Calories: Daily calorie needs based on the Harris-Benedict equation
    """
    if sex == 0:
        calories = (66 + (6.23 * weight) + (12.7 * height) - (6.8 * age)) * activity_level
    else:
        calories = (655 + (4.35 * weight) + (4.7 * height) - (4.7 * age)) * activity_level
    return calories


@require_POST
def logout_view(request):
    logout(request)
    # Redirect to a success page, such as the home page or login page after logout
    return HttpResponseRedirect(reverse('login'))


def index(request):
    return redirect("../demo/login")


class Register(FormView):
    template_name = 'accounts/register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')  # Use reverse_lazy for class-based view attributes

    def form_valid(self, form):
        form.save()  # Save the user
        return super().form_valid(form)


class Account(LoginRequiredMixin, View):
    template_name = 'accounts/account.html'

    def get(self, request, *args, **kwargs):
        weight = request.user.profile.weight
        height = request.user.profile.height
        age = request.user.profile.age
        sex = request.user.profile.sex
        activity_level = request.user.profile.activity_level

        calories = calculate_calories(weight, height, age, sex, activity_level)

        user_protein = calories / 4
        user_carbs = calories / 4
        user_fat = calories / 9
        user_sugar = 36.0 if sex == 0 else 25.0  # Added sugar limit in grams
        user_sodium = 2300.0

        profile_form = ProfileForm(instance=request.user.profile)
        preferences_form = UserPreferencesForm(instance=request.user.userpreferences)
        allergies_form = UserAllergiesForm(instance=request.user.userallergies)
        apikeys_form = UserAPIkeysForm(instance=request.user.userapikeys)

        context = {
            'profile_form': profile_form,
            'preferences_form': preferences_form,
            'allergies_form': allergies_form,
            'apikeys_form': apikeys_form,
            'protein': user_protein,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        preferences_form = UserPreferencesForm(request.POST, instance=request.user.userpreferences)
        allergies_form = UserAllergiesForm(request.POST, instance=request.user.userallergies)
        apikeys_form = UserAPIkeysForm(request.POST, instance=request.user.userapikeys)

        forms = [profile_form, preferences_form, allergies_form, apikeys_form]

        if all(form.is_valid() for form in forms):
            for form in forms:
                form.save()
            return redirect('account')  # Redirect to a success page or profile page
        else:
            for form in forms:
                if form.errors:
                    print(form.errors)  # Logging the form errors can be helpful

        context = {
            'profile_form': profile_form,
            'preferences_form': preferences_form,
            'allergies_form': allergies_form,
            'apikeys_form': apikeys_form
        }
        return render(request, self.template_name, context)
