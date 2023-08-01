from django.urls import path, include

from .views import register, dashboard




app_name = 'accounts'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('register/', register, name='register'),
]