from rest_framework import permissions


class PatientOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_patient:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_patient:
            return True
        return False


class DoctorOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_doctor:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.account_type == "D":
            return True
        return False
