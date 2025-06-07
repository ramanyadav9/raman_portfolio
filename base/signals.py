from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email,
        )
        print("Profile created for:", instance.email)


@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    if not created:
        profile = getattr(instance, 'profile', None)
        if profile:
            profile.first_name = instance.first_name
            profile.last_name = instance.last_name
            profile.email = instance.email
            profile.save()
            print("Profile updated for:", instance.email)


@receiver(pre_save, sender=User)
def update_username(sender, instance, **kwargs):
    if instance.email:
        instance.username = instance.email
        print("Username updated to email for:", instance.email)
