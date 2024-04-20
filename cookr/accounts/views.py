from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import SignUpForm

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})
