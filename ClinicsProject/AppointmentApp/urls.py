from django.urls import path

from .views import (BookAppointment, Doctor_All_Appointments_API,
                    DoctorAppointmentsListView, Patient_All_Appointments_API,
                    PatientAppointmentsListView, Rating, appointment_details,
                    complete, doctor_cancel, patient_appointment_details,
                    patient_cancel)

urlpatterns = [
    path("book_appointment/<int:pk>/", BookAppointment.as_view(), name="appointment"),
    path(
        "appointmentlist/<int:id>/",
        DoctorAppointmentsListView.as_view(),
        name="appointmentlist",
    ),
    path(
        "patient_appointmentlist/<int:id>/",
        PatientAppointmentsListView.as_view(),
        name="patient_appointmentlist",
    ),
    path("cancel2/<int:id>/", patient_cancel, name="patient_cancel"),
    path("cancel/<int:id>/", doctor_cancel, name="doctor_cancel"),
    path("completed/<int:id>/", complete, name="complete"),
    path("rate/<int:id>/", Rating, name="rating"),
    path(
        "appointment_details/<int:id>/",
        appointment_details,
        name="doctor_appointment_details",
    ),
    path(
        "patient_appointment_details/<int:id>/",
        patient_appointment_details,
        name="patient_appointment_details",
    ),
    path("patient_all_appointment_api/", Patient_All_Appointments_API.as_view()),
    path("doctor_all_appointment_api/", Doctor_All_Appointments_API.as_view()),
]
