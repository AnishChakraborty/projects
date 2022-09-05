from django.core.management import BaseCommand

from DoctorApp.models import Specialisation


class Command(BaseCommand):
    help = "add specilization"

    def handle(self, *args, **options):
        l = ["dentist", "ent"]
        for i in l:
            s = Specialisation.objects.create(specialisation=i)
            s.save()
