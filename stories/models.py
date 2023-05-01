from django.db import models
from accounts.models import User
from storages.backends.s3boto3 import S3Boto3Storage


# Create your models here.
class Stories(models.Model):
    video = models.FileField(storage=S3Boto3Storage(), upload_to="stories/")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    viewers = models.ManyToManyField(User, related_name="viewers", blank=True)
