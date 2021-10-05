from django.contrib import admin
from .models import (
    CustomUser,
    Track,
    Topic,
    Course,
    Resource,
    UserTrackBridge,
    TrackTopicBridge,
    TopicCourseBridge,
    UserProgress,
    Profile,
    Project,
)

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Track)
admin.site.register(Topic)
admin.site.register(Course)
admin.site.register(Resource)
admin.site.register(UserTrackBridge)
admin.site.register(TrackTopicBridge)
admin.site.register(TopicCourseBridge)
admin.site.register(UserProgress)
admin.site.register(Profile)
admin.site.register(Project)



