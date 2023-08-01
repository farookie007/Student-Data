from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CustomUserCreationForm



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You\'ll be redirected to login')
            return redirect(reverse('user_auth:login'))
        form = CustomUserCreationForm(request.POST)
        messages.warning(request, "Invalid parameters")
        return render(request, 'accounts/register.html', {'form': form})
    form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')