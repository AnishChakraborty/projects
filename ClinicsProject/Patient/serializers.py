from rest_framework import serializers

from AuthuserApp.models import User
from AuthuserApp.serializers import UserSerializer

from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True, required=True)

    class Meta:
        model = Patient
        fields = (
            "user",
            "age",
            "addhar_id",
            "address",
            "nationality",
            "dob",
            "gender",
            "file",
        )


class PatientRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Patient
        fields = (
            "user",
            "age",
            "addhar_id",
            "address",
            "nationality",
            "dob",
            "gender",
            "file",
        )
        extra_kwargs = {"firstname": {"required": True}}

    def create(self, validated_data):
        data = validated_data.pop("user")
        user = User.objects.create_user(**data)
        user.save()
        patient = Patient(
            user=user,
            age=validated_data.pop("age"),
            gender=validated_data.pop("gender"),
            dob=validated_data.pop("dob"),
            phone_no=validated_data.pop("phone_no"),
            nationality=validated_data.pop("nationality"),
            address=validated_data.pop("address"),
            addhar_id=validated_data.pop("addhar_id"),
        )
        patient.save()
        return patient
