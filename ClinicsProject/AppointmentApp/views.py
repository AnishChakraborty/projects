from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import (HttpResponse, HttpResponseRedirect, redirect,
                              render, reverse)
from django.views.generic import ListView, TemplateView
from rest_framework import filters, generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from AuthuserApp.models import User
from DoctorApp.models import Doctor
from DoctorApp.permissons import DoctorOnly, PatientOnly
from Patient.decoraters import (DoctorPermissionsMixin,
                                PatientPermissionsMixin,
                                authenticate_doctor_user,
                                authenticate_patient_user)
from Patient.views import MyPagination

from .forms import AppointmentForm, RatingForm
from .models import Appointment
from .serializers import AppointmentSerializer

# Create your views here.
for user in User.objects.all():
    Token.objects.get_or_create(user=user)


class BookAppointment(PatientPermissionsMixin, TemplateView):
    template_name = "appointment/appointment.html"

    def post(self, request, *args, **kwargs):
        ctx = super().get_context_data()
        post_data = request.POST
        form = AppointmentForm(post_data)
        patient = request.user
        doctor = User.objects.get(id=kwargs["pk"])
        if form.is_valid():
            a = form.save(commit=False)
            a.doctor = doctor
            a.patient = patient
            a.status = "pending"
            a.location = doctor.doctor.address
            a.save()
            return redirect("home")
        ctx["form"] = form
        return self.render_to_response(ctx)

    def get(self, request, *args, **kwargs):
        all_doctors = Doctor.objects.all()
        form = AppointmentForm
        ctx = super().get_context_data()
        ctx["doctors"] = all_doctors
        ctx["form"] = form
        return self.render_to_response(ctx)


class DoctorAppointmentsListView(DoctorPermissionsMixin, ListView):
    paginate_by = 2
    template_name = "appointment/da_list.html"

    def get_queryset(self):
        queryset = Appointment.objects.filter(doctor=self.request.user)
        return queryset


class PatientAppointmentsListView(PatientPermissionsMixin, ListView):
    paginate_by = 2
    template_name = "appointment/pa_list.html"

    def get_queryset(self):
        queryset = Appointment.objects.filter(patient=self.request.user)
        return queryset


@authenticate_patient_user
@login_required(login_url="patient_login")
def patient_cancel(request, id):
    appointment = Appointment.objects.get(id=id)
    appointment.status = "canceled"
    appointment.save()
    return redirect("patient_appointmentlist", id)


@authenticate_doctor_user
@login_required(login_url="login")
def doctor_cancel(request, id):
    appointment = Appointment.objects.get(id=id)
    appointment.status = "canceled"
    appointment.save()
    return redirect("appointmentlist", id)


@authenticate_doctor_user
@login_required(login_url="login")
def complete(request, id):
    appointment = Appointment.objects.get(id=id)
    appointment.status = "completed"
    appointment.save()
    return redirect("appointmentlist", id)


@authenticate_patient_user
def Rating(request, id):
    appointment = Appointment.objects.get(id=id)
    patient = request.user
    pk = patient.id
    form = RatingForm()
    if request.method == "POST":
        form = RatingForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect("patient_appointmentlist", pk)
    return render(request, "appointment/rate.html", {"form": form})


@authenticate_doctor_user
@login_required(login_url="login")
def appointment_details(request, id):
    obj = Appointment.objects.get(id=id)
    ctx = {"obj": obj}
    return render(request, "appointment/appointment_details.html", ctx)


@authenticate_patient_user
@login_required(login_url="patient_login")
def patient_appointment_details(request, id):
    obj = Appointment.objects.get(id=id)
    ctx = {"obj": obj}
    return render(request, "appointment/patient_appointment_details.html", ctx)


class Patient_All_Appointments_API(DoctorPermissionsMixin, generics.ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        try:
            return Appointment.objects.filter(patient=self.request.user)
        except Appointment.DoesNotExist:
            raise Http404

    filter_backends = [filters.SearchFilter]
    search_fields = ["location", "appointment_date", "status", "rating"]
    pagination_class = MyPagination
    permission_classes = [PatientOnly]


class Doctor_All_Appointments_API(DoctorPermissionsMixin, generics.ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        try:
            return Appointment.objects.filter(doctor=self.request.user)
        except Appointment.DoesNotExist:
            raise Http404

    filter_backends = [filters.SearchFilter]
    search_fields = ["location", "appointment_date", "status", "rating"]
    pagination_class = MyPagination
    permission_classes = [DoctorOnly]
