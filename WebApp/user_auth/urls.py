from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

# from .views import login




app_name = 'user_auth'

urlpatterns = [
    path('', LoginView.as_view(template_name='user_auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='user_auth/logout.html'), name='logout')
]