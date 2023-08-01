from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(blank=True, unique=True, null=False)
    username = models.CharField(max_length=100, unique=True, null=False)
    first_name = models.CharField(max_length=100, blank=True, null=False)
    last_name = models.CharField(max_length=100, blank=True, null=False)
    middle_name = models.CharField(max_length=100, blank=True)
    school = models.CharField(max_length=150, blank=True)
    cgpa = models.FloatField(max_length=5, default=0.00)
    std_mail = models.CharField(max_length=150, blank=True)
    faculty = models.CharField(max_length=150, blank=True)
    department = models.CharField(max_length=150, blank=True)


    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    @property
    def matric(self):
        return self.username

    def __str__(self):
        return f"{self.matric} - {self.email}"
    
    def save(self, *args, **kwargs):
        # to convert all matric number entries to uppercase
        self.username = self.username.upper()
        super().save(*args, **kwargs)
