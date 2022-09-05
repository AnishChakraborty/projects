from rest_framework import serializers

from AuthuserApp.models import User
from AuthuserApp.serializers import UserSerializer

from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Doctor
        fields = [
            "user",
            "age",
            "gender",
            "fees",
            "specility",
            "address",
            "file",
            "experience",
        ]


class DoctorRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Doctor
        fields = [
            "user",
            "age",
            "gender",
            "fees",
            "specility",
            "address",
            "file",
            "experience",
        ]

    def create(self, validated_data):
        data = validated_data.pop("user")
        user = User.objects.create_user(**data)
        user.save()
        doctor = Doctor(
            user=user,
            age=validated_data.pop("age"),
            gender=validated_data.pop("gender"),
            fees=validated_data.pop("fees"),
            specility=validated_data.pop("specility"),
            address=validated_data.pop("address"),
            experience=validated_data.pop("experience"),
            phone_no=validated_data.pop("phone_no"),
            file=validated_data.pop("file"),
        )
        doctor.save()
        return doctor
