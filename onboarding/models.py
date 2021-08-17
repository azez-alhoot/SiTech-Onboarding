from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
 
    title = models.CharField(max_length = 50)
    image = models.ImageField(upload_to = 'user_photos')

    def __str__(self):
        return self.username


class Track(models.Model):
    track_name = models.CharField(max_length = 50)

    def __str__(self):
        return self.track_name
