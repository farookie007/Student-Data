from django.urls import path, include

from .views import upload_result_view




app_name = 'results'

urlpatterns = [
    path('upload/', upload_result_view, name='upload'),
]