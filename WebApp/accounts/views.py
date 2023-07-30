from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .forms import CustomUserCreationForm



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You\'ll be redirected to login')
            return redirect(reverse('user_auth:login'))

    form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
