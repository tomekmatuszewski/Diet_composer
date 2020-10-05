from django.contrib import admin

from .models import Profile, UserActivity

admin.site.register(Profile)
admin.site.register(UserActivity)
