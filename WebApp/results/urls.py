from django.urls import path, include

from .views import upload_result_view




urlpatterns = [
    path('upload/', upload_result_view, name='results_upload'),
]