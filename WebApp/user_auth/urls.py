from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import login_view




app_name = 'user_auth'

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', LogoutView.as_view(template_name='user_auth/logout.html'), name='logout')
]