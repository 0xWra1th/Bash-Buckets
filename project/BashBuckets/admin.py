from django.contrib import admin
from .models import User, Bucket, UserBucket, AppToken

# Registration of models for display on admin page
admin.site.register(User)
admin.site.register(Bucket)
admin.site.register(UserBucket)
admin.site.register(AppToken)