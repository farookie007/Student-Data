from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import AuthenticationForm

from .forms import LoginForm



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            matric = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # getting the auto-generated username using the matric_no
            # user = get_user_model().objects.filter(matric=matric).first()
            user = authenticate(request, username=matric, password=password)
            print(user)
            if user is not None:
                login(request)
                messages.success(request, f'Login successful')
                return redirect(reverse('accounts:dashboard'))
        messages.error(request, 'Invalid matric number or password')
        form = LoginForm(request.POST)
    else:
        form = LoginForm()
    return render(request, 'user_auth/login.html', {'form': form})
