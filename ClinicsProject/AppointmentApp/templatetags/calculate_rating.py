from django import template

from AppointmentApp.models import Appointment

register = template.Library()


@register.filter
def rating(obj):
    doc_id = obj.id
    appointments = Appointment.objects.filter(doctor_id=doc_id).filter(
        rating__isnull=False
    )
    total = 0
    count = 0
    for a in appointments:
        total += int(a.rating)
        count += 1
    if appointments:
        return f"{total/count:.1f}"
    return 0
