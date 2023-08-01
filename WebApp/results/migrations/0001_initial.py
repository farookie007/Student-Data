# Generated by Django 4.2.3 on 2023-08-01 10:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Result",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("semester", models.CharField(blank=True, max_length=20)),
                ("result_id", models.CharField(blank=True, max_length=30, unique=True)),
                ("level", models.CharField(blank=True, max_length=5)),
                ("session", models.CharField(blank=True, max_length=20)),
                ("payload", models.JSONField()),
                ("gpa", models.FloatField(default=0.0, max_length=5)),
                ("cgpa", models.FloatField(default=0.0, max_length=5)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
