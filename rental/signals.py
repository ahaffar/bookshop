from django.dispatch import receiver
from django.db.models import signals
from django.contrib.auth import get_user_model
from rental.models import UserProfile

User = get_user_model()


@receiver(signals.post_save, sender=User)
def create_or_update_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(signals.post_save, sender=User)
def update_userprofile(sender, instance, **kwargs):
    instance.profile.save()