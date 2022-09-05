from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import (HttpResponse, HttpResponseRedirect, redirect,
                              render)
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView
from rest_framework import filters, generics, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)
from rest_framework.views import APIView

from AuthuserApp.models import User
from DoctorApp.models import Doctor
from DoctorApp.permissons import PatientOnly
from DoctorApp.serializers import DoctorSerializer

from .decoraters import PatientPermissionsMixin, authenticate_patient_user
from .filters import DoctorFilter
from .forms import (LoginForm, PatientForm, ProfileUpdateForm,
                    RegisterPatientForm, Userform,RegisterForm)
from .models import Patient
from .serializers import PatientRegisterSerializer, PatientSerializer


class Register(TemplateView):
    template_name = "Patient/register.html"
    def get(self, request, *arg, **kwargs):
        ctx = super().get_context_data()
        form = RegisterPatientForm
        form1 = PatientForm
        ctx["form"] = form
        ctx["form1"] = form1
        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data()
        form = RegisterPatientForm(request.POST)
        form1 = PatientForm(request.POST)
        if form.is_valid() and form1.is_valid():
            user = User.objects.create_user(
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password"],
                    phone_no=form.cleaned_data["phone_no"],
                )
            user.is_active = True
            user.firstname = form.cleaned_data["firstname"]
            user.lastname = form.cleaned_data["lastname"]
            user.phone_no = form.cleaned_data["phone_no"]
            user.save()
            profile = Patient(
                    user=user,
                    age=form1.cleaned_data["age"],
                    gender=form1.cleaned_data["gender"],
                    dob=form1.cleaned_data["dob"],
                    nationality=form1.cleaned_data["nationality"],
                    address=form1.cleaned_data["address"],
                    addhar_id=form1.cleaned_data["addhar_id"],
                    )
            profile.save()
            context["form"] = form
            context["form1"] = form1
            return self.render_to_response(context)
        else:
            ctx = super().get_context_data()
            ctx["form"] = form
            ctx["form1"] = form1
            return self.render_to_response(ctx)



class Login(TemplateView):
    template_name = "Patient/login.html"

    def get(self, request, *args, **kwargs):
        ctx = super().get_context_data()
        form = LoginForm
        ctx["form"] = form
        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
        messages.error(request, "username or password is not valid")
        return redirect("patient_login")

def logout_request(request):
    logout(request)
    return redirect("HOME")


@authenticate_patient_user
@login_required(login_url="patient_login")
def profile(request):
    if request.user.account_type == "P":
        return render(request, "Patient/profile.html")


class PatientPage(TemplateView):
    model = Patient
    template_name = "Patient/patient.html"


@authenticate_patient_user
@login_required(login_url="patient_login")
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "password successfully updated")
            return redirect("patient_profile")
        else:
            messages.error(request, "please fulfill the below requirements")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "Patient/change_password.html", {"form": form})


@authenticate_patient_user
@login_required(login_url="patient_login")
def doctorlist(request):
    if request.user.account_type == "P":
        doctors = Doctor.objects.all()
        context = {}
        myfilter = DoctorFilter(request.GET, queryset=doctors)
        doctor = myfilter.qs
        paginator = Paginator(doctor, 1)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["myfilter"] = myfilter
        context["doctors"] = doctors
        context["page_obj"] = page_obj
        return render(request, "Patient/doctors.html", context)


class Update_patient_Profile(PatientPermissionsMixin, LoginRequiredMixin, TemplateView):
    form1 = Userform
    form2 = ProfileUpdateForm
    template_name = "Patient/update.html"

    def post(self, request, *args, **kwargs):
        context = super().get_context_data()
        post_data = request.POST
        form1 = Userform(post_data)
        form2 = ProfileUpdateForm(post_data, request.FILES)
        context["form1"] = form1
        context["form2"] = form2
        if form1.is_valid() and form2.is_valid():
            request.user.firstname = form1.cleaned_data["firstname"]
            request.user.lastname = form1.cleaned_data["lastname"]
            request.user.save()
            request.user.patient.age = form2.cleaned_data["age"]
            request.user.patient.addhar_id = form2.cleaned_data["addhar_id"]
            request.user.patient.address = form2.cleaned_data["address"]
            request.user.patient.nationality = form2.cleaned_data["nationality"]
            request.user.patient.dob = form2.cleaned_data["dob"]
            request.user.patient.gender = form2.cleaned_data["gender"]
            request.user.patient.file = form2.cleaned_data["file"]
            request.user.patient.save()
            context["form1"] = form1
            context["form2"] = form2
            return redirect("patient_profile")
        else:
            ctx = super().get_context_data()
            form1 = Userform(instance=request.user)
            form2 = ProfileUpdateForm(instance=request.user.patient)
            ctx["form1"] = form1
            ctx["form2"] = form2
            return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        ctx = super().get_context_data()
        form1 = Userform(instance=request.user)
        form2 = ProfileUpdateForm(instance=request.user.patient)
        ctx["form1"] = form1
        ctx["form2"] = form2
        return self.render_to_response(ctx)


class Home(PatientPermissionsMixin, TemplateView):
    template_name = "Patient/patienthome.html"


@authenticate_patient_user
@login_required(login_url="patient_login")
def doctor_profile(request, id):
    if request.user.account_type == "P":
        user = User.objects.get(id=id)
        ctx = {"user": user}
        return render(request, "Patient/d_profile.html", ctx)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = PatientRegisterSerializer


class MyPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = "page_size"
    last_page_strings = ("the_end",)


class Find_Doctor(generics.ListAPIView):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["specility", "address"]
    pagination_class = MyPagination
    permission_classes = [PatientOnly]


class Doctor_Details_API(APIView):
    serializer_class = DoctorSerializer

    def get_object(self, pk):
        try:
            return Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        doctor = self.get_object(pk)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

    permission_classes = PatientOnly
