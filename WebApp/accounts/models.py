from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    matric = models.CharField(max_length=15, blank=True, unique=True)
    email = models.EmailField(blank=True, unique=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    school = models.CharField(max_length=150, blank=True)
    cgpa = models.FloatField(max_length=5, default=0.00)
    std_mail = models.CharField(max_length=150, blank=True)
    faculty = models.CharField(max_length=150, blank=True)
    department = models.CharField(max_length=150, blank=True)


    REQUIRED_FIELDS = ['email', 'matric', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.matric} - {self.email}"
