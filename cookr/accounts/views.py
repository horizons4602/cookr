from django.shortcuts import redirect, render
from django.views.generic import View
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, ProfileForm, UserPreferencesForm, UserAllergiesForm, UserAPIkeysForm


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
        profile_form = ProfileForm(instance=request.user.profile)
        preferences_form = UserPreferencesForm(instance=request.user.userpreferences)
        allergies_form = UserAllergiesForm(instance=request.user.userallergies)
        apikeys_form = UserAPIkeysForm(instance=request.user.userapikeys)

        context = {
            'profile_form': profile_form,
            'preferences_form': preferences_form,
            'allergies_form': allergies_form,
            'apikeys_form': apikeys_form
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

        # If forms are not valid, re-render the page with error messages
        context = {
            'profile_form': profile_form,
            'preferences_form': preferences_form,
            'allergies_form': allergies_form,
            'apikeys_form': apikeys_form
        }
        return render(request, self.template_name, context)