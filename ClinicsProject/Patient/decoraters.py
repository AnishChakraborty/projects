from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


def authenticate_patient_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_patient:
            return view_function(request, *args, **kwargs)
        else:
            return PermissionDenied()
    return wrapper_function


def authenticate_doctor_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if not request.user.is_doctor:
            return view_function(request, *args, **kwargs)
        else:
            raise PermissionDenied()
    return wrapper_function


class DoctorPermissionsMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        if not request.user.is_doctor:
            raise PermissionDenied()
        return super(DoctorPermissionsMixin, self).dispatch(request, *args, **kwargs)


class PatientPermissionsMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        if not request.user.is_patient:
            raise PermissionDenied()
        return super(PatientPermissionsMixin, self).dispatch(request, *args, **kwargs)