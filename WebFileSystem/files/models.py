from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class FolderManager(models.Manager):
    def for_user(self, user):
        return self.filter(user=user)


class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="folders")
    name = models.CharField(max_length=255)
    parent_folder = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name="subfolders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)  # Add this
    deleted_at = models.DateTimeField(null=True, blank=True)  # Add this for trash functionality
    objects = FolderManager()

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        # Move to trash or delete entirely
        if kwargs.get('permanent', False):  # Permanent delete
            self.subfolders.all().delete(permanent=True)
            self.files.all().delete()
            super().delete(*args, **kwargs)
        else:  # Move to trash
            self.is_deleted = True
            self.deleted_at = now()
            self.save()
            for subfolder in self.subfolders.all():
                subfolder.delete()
            for file in self.files.all():
                file.mark_as_deleted()

class UploadedFile(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="files")
    original_name = models.CharField(max_length=255)  # Stores the original file name
    file = models.FileField(upload_to="uploaded_files/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def mark_as_deleted(self):
        self.is_deleted = True
        self.deleted_at = now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def save(self, *args, **kwargs):
        # Store the original file name when saving
        if not self.original_name and self.file:
            self.original_name = self.file.name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.original_name
