from django.contrib import admin
from .models import CustomUser, Track, Topic, Course, Resources, UserTrackBridge

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Track)
admin.site.register(Topic)
admin.site.register(Course)
admin.site.register(Resources)
admin.site.register(UserTrackBridge)
