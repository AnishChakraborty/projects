from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, UpdateView)
from rest_framework import generics

from AuthuserApp.models import User
from Patient.decoraters import DoctorPermissionsMixin, authenticate_doctor_user
from Patient.models import Patient

from .forms import (DoctorForm, Form1, LoginForm, RegisterDoctortForm,
                    UpdateForm, Updateform2)
from .models import Doctor
from .serializers import DoctorRegisterSerializer


class Register(TemplateView):
    template_name = "DoctorApp/register.html"

    def get(self, request, *arg, **kwargs):
        context = super().get_context_data()
        form = RegisterDoctortForm
        form1 = DoctorForm
        context["form"] = form
        context["form1"] = form1
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data()
        form = RegisterDoctortForm(request.POST)
        form1 = DoctorForm(request.POST)
        if form.is_valid() and form1.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
                phone_no=form.cleaned_data["phone_no"],
                account_type="D",
            )
            user.is_active = True
            user.firstname = form.cleaned_data["firstname"]
            user.lastname = form.cleaned_data["lastname"]
            user.save()
            user.account_type = "D"
            profile = Doctor(
                user=user,
                gender=form1.cleaned_data["gender"],
                age=form1.cleaned_data["age"],
                fees=form1.cleaned_data["fees"],
                specility=form1.cleaned_data["specility"],
                address=form1.cleaned_data["address"],
            )
            profile.save()
        context["form"] = form
        context["form1"] = form1
        return self.render_to_response(context)


class Login(TemplateView):
    template_name = "DoctorApp/login.html"

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
                return redirect("doctor_home")
        messages.error(request, "username or password is not valid")
        return redirect("doctor_login")


def logout_request(request):
    logout(request)
    return redirect("HOME")


@login_required(login_url="doctor_login")
@authenticate_doctor_user
def profile(request):
    if request.user.account_type == "D":
        return render(request, "DoctorApp/detail.html")


class DoctorPage(TemplateView):
    model = Doctor
    template_name = "DoctorApp/doctor.html"


@login_required(login_url="doctor_login")
@authenticate_doctor_user
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "password successfully updated")
            return redirect("profile")
        else:
            messages.error(request, "please fulfill the below requirements")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "DoctorApp/change_password.html", {"form": form})


class UpdateProfile(DoctorPermissionsMixin, TemplateView):
    form1 = UpdateForm
    form2 = Updateform2
    template_name = "DoctorApp/update.html"

    def post(self, request, *args, **kwargs):
        context = super().get_context_data()
        post_data = request.POST
        form1 = UpdateForm(post_data)
        form2 = Updateform2(post_data, request.FILES)
        context["form1"] = form1
        context["form2"] = form2
        if form1.is_valid() and form2.is_valid():
            request.user.firstname = form1.cleaned_data["firstname"]
            request.user.lastname = form1.cleaned_data["lastname"]
            request.user.save()
            request.user.doctor.fees = form2.cleaned_data["fees"]
            request.user.doctor.address = form2.cleaned_data["address"]
            request.user.doctor.specility = form2.cleaned_data["specility"]
            request.user.doctor.gender = form2.cleaned_data["gender"]
            request.user.doctor.file = form2.cleaned_data["file"]
            request.user.doctor.save()
            context["form1"] = form1
            context["form2"] = form2
            return redirect("profile")
        else:
            ctx = super().get_context_data()
            form1 = UpdateForm(instance=request.user)
            form2 = Updateform2(instance=request.user.doctor)
            ctx["form1"] = form1
            ctx["form2"] = form2
            return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        ctx = super().get_context_data()
        form1 = UpdateForm(instance=request.user)
        form2 = Updateform2(instance=request.user.doctor)
        ctx["form1"] = form1
        ctx["form2"] = form2
        return self.render_to_response(ctx)


@authenticate_doctor_user
@login_required(login_url="doctor_login")
def patient_profile(request, id):
    if request.user.account_type == "D":
        user = User.objects.get(id=id)
        ctx = {"user": user}
        return render(request, "DoctorApp/p_profile.html", ctx)


class Home(DoctorPermissionsMixin, TemplateView):
    template_name = "DoctorApp/doctorhome.html"


class RegisterView(generics.CreateAPIView):
    serializer_class = DoctorRegisterSerializer
    queryset = User.objects.all()
