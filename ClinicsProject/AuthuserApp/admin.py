from django.contrib import admin

from DoctorApp.models import Specialisation

from .models import User

# Register your models here.
admin.site.register(User)
admin.site.register(Specialisation)
