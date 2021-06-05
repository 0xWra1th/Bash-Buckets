from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# The User model overrides the standard Django Auth User model, for keeping track of bucket owner(admin) tokens.
class User(AbstractUser):
    token = models.UUIDField(default=uuid.uuid4, editable=False)

# Bucket model, for keeping track of directories
class Bucket(models.Model):
    name = models.CharField(max_length=50)
    path = models.CharField(max_length=50)

# UserBuckets model, for keeping track who owns buckets
class UserBucket(models.Model):
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# AppToken model, for keeping track of created Application Tokens
class AppToken(models.Model):
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)