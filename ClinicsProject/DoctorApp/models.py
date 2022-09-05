from django.db import models
from django.db.models.signals import post_save, pre_save
from rest_framework.authtoken.models import Token

from AuthuserApp.models import User


# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    specility = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    experience = models.IntegerField(default=0)
    fees = models.FloatField(default=0.0)
    GENDER_CHOICES = (("M", "Male"), ("F", "Female"), ("O", "Others"))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="m")
    file = models.FileField(null=True)

    def __str__(self):
        return self.user.firstname


class Specialisation(models.Model):
    specialisation = models.CharField(max_length=10)


def pre_save_signal(sender, instance, **kwargs):
    print("before register doctor")


def post_save_signal(sender, instance, **kwargs):
    print("you successfully registered doctor")


pre_save.connect(pre_save_signal, sender=Doctor)
post_save.connect(post_save_signal, sender=Doctor)
