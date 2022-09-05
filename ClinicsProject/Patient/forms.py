from django import forms
from AuthuserApp.models import User
from Patient.models import Patient
from django.forms import ValidationError


class RegisterPatientForm(forms.ModelForm):
    confirm_password = forms.CharField()
    class Meta:
        model = User
        fields = ["email", "password","confirm_password","firstname", "lastname", "phone_no"]

    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password==confirm_password:
            return cleaned_data
        else:
            raise ValidationError("passwords not match")

    def clean_username(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=self.cleaned_data['username']).exists():
            raise ValidationError("exist email")
        else:
            return email

    def clean_phone_no(self):
        phone_no = self.cleaned_data['phone_no']
        if User.objects.filter(phone_no=self.cleaned_data['phone_no']).exists():
            raise ValidationError("exist phone number")
        else:
            return phone_no

class RegisterForm(forms.Form):
    email = forms.EmailField(max_length=50)
    password = forms.CharField(max_length=15)
    confirm_password = forms.CharField(max_length=15)
    firstname = forms.CharField(max_length=30)
    lastname = forms.CharField(max_length=30)
    phone_no = forms.CharField(max_length=12)


class PatientForm(forms.Form):
    age = forms.IntegerField(max_value=90, min_value=1)
    addhar_id = forms.CharField(max_length=14)
    address = forms.CharField(max_length=50)
    nationality = forms.CharField(max_length=20)
    dob = forms.DateTimeField()
    GENDER_CHOICES = (("M", "Male"), ("F", "Female"), ("O", "Others"))
    gender = forms.ChoiceField(choices=GENDER_CHOICES)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=15)

    def clean_username(self):
        data = self.cleaned_data["username"]
        if "@" in data:
            return data
        else:
            data = User.objects.get(phone_no=data).email
            return data


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["age", "addhar_id", "address", "nationality", "dob", "gender", "file"]


class Userform(forms.ModelForm):
    class Meta:
        model = User
        fields = ["firstname", "lastname"]
