from django.urls import path
from rest_framework.authtoken import views

from .views import (Doctor_Details_API, Find_Doctor, Home, Login, PatientPage,
                    Register, RegisterView, Update_patient_Profile,
                    change_password, doctor_profile, doctorlist,
                    logout_request, profile)

urlpatterns = [
    path("patient/signup/", Register.as_view(), name="patient_signup"),
    path("patient/login/", Login.as_view(), name="patient_login"),
    path("patient/update/", Update_patient_Profile.as_view(), name="patient_update"),
    path("patient/logout/", logout_request, name="patientlogout"),
    path("patient/profile/", profile, name="patient_profile"),
    path("patientpage/", PatientPage.as_view(), name="patient"),
    path("", Home.as_view(), name="home"),
    path("patient/changepassword", change_password, name="patient_changepassword"),
    path("doctorlist/", doctorlist, name="doctors"),
    path("doctor_profile/<int:id>/", doctor_profile, name="doctorprofile"),
    path("registration_api/", RegisterView.as_view()),
    path("find_doctor_api/", Find_Doctor.as_view()),
    path("doctor_details_api/<int:pk>/", Doctor_Details_API.as_view()),
    path("api-token-auth/", views.obtain_auth_token),
]
