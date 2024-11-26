from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Folder

@receiver(post_save, sender=User)
def create_default_folder(sender, instance, created, **kwargs):
    """
    Signal to create a default folder for a user after they are created.
    """
    if created:  # Only create the folder for new users
        Folder.objects.create(user=instance, name="Default Folder")
