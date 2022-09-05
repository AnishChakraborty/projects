from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from .manager import CustomeManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    accounts = (("D", "Doctor"), ("P", "Patient"))
    email = models.EmailField(_("email address"), unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    is_staff = models.BooleanField(default=True)
    firstname = models.CharField(max_length=50, null=True)
    lastname = models.CharField(max_length=50, null=True)
    objects = CustomeManager()
    is_active = models.BooleanField(default=True)
    account_type = models.CharField(choices=accounts, default="P", max_length=1)
    phone_no = models.CharField(max_length=13, unique=True)

    class Meta:
        order_with_respect_to = "firstname"

    @property
    def is_doctor(self):
        if self.account_type == "D":
            return True

    @property
    def is_patient(self):
        if self.account_type == "P":
            return True
