from django.contrib import admin
from .models import CustomUser, Track, Topic

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Track)
admin.site.register(Topic)

