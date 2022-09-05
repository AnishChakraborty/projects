# Generated by Django 4.0.6 on 2022-08-25 02:38

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Appointment",
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
                (
                    "appointment_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("location", models.CharField(default="location", max_length=100)),
                ("status", models.CharField(default="Pending", max_length=10)),
                (
                    "rating",
                    models.CharField(
                        choices=[("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5)],
                        max_length=2,
                        null=True,
                    ),
                ),
                ("review", models.CharField(max_length=150, null=True)),
                (
                    "doctor",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_doctor",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_patient",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]