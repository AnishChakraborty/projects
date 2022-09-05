from django.db import models
from django.utils import timezone

from AuthuserApp.models import User
from DoctorApp.models import Doctor
from Patient.models import Patient


# Create your models here.
class Appointment(models.Model):
    choices = (("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5))
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="%(class)s_patient"
    )
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="%(class)s_doctor"
    )
    appointment_date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=100, default="location")
    status = models.CharField(default="Pending", max_length=10)
    rate_choices = (("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5))
    rating = models.CharField(null=True, choices=rate_choices, max_length=2)
    review = models.CharField(null=True, max_length=150)
