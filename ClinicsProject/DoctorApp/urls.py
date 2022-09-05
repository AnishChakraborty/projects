from django.urls import path
from rest_framework.authtoken import views

from .views import (DoctorPage, Home, Login, Register, RegisterView,
                    UpdateProfile, change_password, logout_request,
                    patient_profile, profile)

urlpatterns = [
    path("doctor/register/", Register.as_view(), name="doctor_signup"),
    path("doctor/login", Login.as_view(), name="doctor_login"),
    path("doctor/", DoctorPage.as_view(), name="Doctor"),
    path("doctor/profile/", profile, name="profile"),
    path("/doctor/logout/", logout_request, name="logout"),
    path("changepassword/", change_password, name="changepassword"),
    path("update/", UpdateProfile.as_view(), name="update"),
    path("patient_profile/<int:id>/", patient_profile, name="patient_profile"),
    path("", Home.as_view(), name="doctor_home"),
    path("doctor_register_api/", RegisterView.as_view()),
    path("api-token-auth/", views.obtain_auth_token),
]
