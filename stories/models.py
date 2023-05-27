from django.db import models
from accounts.models import User
from storages.backends.s3boto3 import S3Boto3Storage
import os


# Create your models here.
def stories_location(instance, filename):
    path = os.path.join("users", str(instance.user.id), "stories", filename)
    return path


class Stories(models.Model):
    video = models.FileField(upload_to=stories_location)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    viewers = models.ManyToManyField(User, related_name="viewers", blank=True)
