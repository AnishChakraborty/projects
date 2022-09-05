from django import forms

from AuthuserApp.models import User

from .models import Doctor

from django.forms import ValidationError


class RegisterDoctortForm(forms.ModelForm):
    confirm_password = forms.CharField()
    class Meta:
        model = User
        fields = ["email", "password", "confirm_password","firstname", "lastname", "phone_no"]

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


class DoctorForm(forms.Form):
    age = forms.IntegerField()
    GENDER_CHOICES = (("M", "Male"), ("F", "Female"), ("O", "Others"))
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    fees = forms.IntegerField()
    specility = forms.CharField(max_length=50)
    address = forms.CharField(max_length=100)


class Form1(forms.Form):
    firstname = forms.CharField(max_length=30)
    lastname = forms.CharField(max_length=30)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)

    def clean_username(self):
        data = self.cleaned_data["username"]
        print(data)
        if "@" in data:
            return data
        else:
            data = User.objects.get(phone_no=data).email
            return data


class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["firstname", "lastname"]


class Updateform2(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ["age", "gender", "fees", "specility", "address", "file", "experience"]
