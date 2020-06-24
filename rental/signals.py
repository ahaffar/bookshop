from django.dispatch import receiver
from django.db.models import signals
from django.contrib.auth import get_user_model
from rental.models import UserProfile, Borrowed, Book
from datetime import datetime, timedelta
from django.utils.text import slugify

User = get_user_model()


@receiver(signals.post_save, sender=User)
def create_or_update_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(signals.post_save, sender=User)
def update_userprofile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(signals.pre_save, sender=Borrowed)
def set_due_back(sender, instance, **kwargs):
    instance.due_back = datetime.now() + timedelta(days=1)


@receiver(signals.pre_save, sender=Book)
def populate_slug(sender, instance, **kwargs):
    instance.slug = slugify(instance.title)
