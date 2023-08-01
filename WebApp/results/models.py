from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Result(models.Model):
    semester = models.CharField(max_length=20, blank=True)
    result_id = models.CharField(max_length=30, blank=True, unique=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='results')
    level = models.CharField(max_length=5, blank=True)
    session = models.CharField(max_length=20, blank=True)
    payload = models.JSONField()
    gpa = models.FloatField(max_length=5, default=0.00)     # stores the gpa of the result
    cgpa = models.FloatField(max_length=5, default=0.00)    # stores the cgpa all previous results

    def __str__(self):
        return f"<Result: {self.level}L | {self.session} | {self.semester}"
