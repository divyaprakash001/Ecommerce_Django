from accounts.models import User
from .models import UserProfile
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=User)
def create_user_profile(sender, instance, **kwargs):
    print("are ye pre save hai")


@receiver(post_save, sender=User)
def create_user_profile_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # create the user profile if not exist or if deleted
            UserProfile.objects.create(user=instance)
            
    #   instance.userprofile.save()


# also connect sender with receiver in this way but we should use decorator for better as per documentation
# post_save.connect(create_user_profile_receiver,sender=User)
