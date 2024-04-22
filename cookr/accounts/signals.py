from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Profile, UserPreferences, UserAllergies, UserAPIkeys
from favorites.models import SavedOne, SavedTwo, SavedThree, SavedFour, SavedFive, SavedSix

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profiles(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        UserPreferences.objects.create(user=instance)
        UserAllergies.objects.create(user=instance)
        UserAPIkeys.objects.create(user=instance)
        SavedOne.objects.create(user=instance)
        SavedTwo.objects.create(user=instance)
        SavedThree.objects.create(user=instance)
        SavedFour.objects.create(user=instance)
        SavedFive.objects.create(user=instance)
        SavedSix.objects.create(user=instance)
