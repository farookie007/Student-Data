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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.matric = self.username     # this ensures that `matric` and `username` fields carry the same value

    @property
    def matric(self):
        """Return the username (i.e the matric number)"""
        return self.username
    
    @matric.setter
    def matric(self, value):
        """Sets the username to value and saves it to the database to maintain uniformity"""
        self.username = value

    def __str__(self):
        return f"{self.matric} - {self.email}"
    
    def save(self, *args, **kwargs):
        # to convert all matric number entries to uppercase
        self.username = self.username.upper()
        super().save(*args, **kwargs)
