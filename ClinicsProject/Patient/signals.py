from django.db.models.signals import post_save

from AuthuserApp.models import User


def save_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(save_profile, sender=User)
