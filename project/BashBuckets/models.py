from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# The User model overrides the standard Django Auth User model, for keeping track of bucket owner(admin) tokens.
class User(AbstractUser):
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    usage_limit = models.IntegerField(default=1024, verbose_name="Usage Limit (MB)")

# Bucket model, for keeping track of directories
class Bucket(models.Model):
    name = models.CharField(max_length=50,unique=True)

# UserBuckets model, for keeping track who owns buckets
class UserBucket(models.Model):
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# AppToken model, for keeping track of created Application Tokens
class AppToken(models.Model):
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)

# Download code, one time links for downloading a file
class DownloadCode(models.Model):
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    path = models.CharField(max_length=1024) # You never know how long paths are...
    code = models.UUIDField(default=uuid.uuid4, editable=False)