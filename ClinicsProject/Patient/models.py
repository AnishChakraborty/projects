from django.db import models
from django.db.models.signals import post_save, pre_save
from rest_framework.authtoken.models import Token
from AuthuserApp.models import User


# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    addhar_id = models.CharField(max_length=16)
    address = models.CharField(max_length=100)
    nationality = models.CharField(max_length=30)
    dob = models.DateTimeField()
    GENDER_CHOICES = (("M", "Male"), ("F", "Female"), ("O", "Others"))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    file = models.FileField(null=True)

    def __str__(self):
        return self.user.firstname


def pre_save_signal(sender, instance, **kwargs):
    print("before register patient")


def post_save_signal(sender, instance, **kwargs):
    print("you successfully registered patient")


pre_save.connect(pre_save_signal, sender=Patient)
post_save.connect(post_save_signal, sender=Patient)