from django.contrib import admin
from .models import CustomUser, Track

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Track)

