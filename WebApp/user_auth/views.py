from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username').upper()
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Login successful')
                return redirect(reverse('accounts:dashboard'))
            messages.error(request, 'Invalid matric number or password')
        else:
            messages.error(request, 'Invalid form submission')
        form = LoginForm(request.POST)
    else:
        form = LoginForm()
    return render(request, 'user_auth/login.html', {'form': form})
