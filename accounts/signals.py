from accounts.models import User
from .models import UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
      instance.userprofile.save()

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):