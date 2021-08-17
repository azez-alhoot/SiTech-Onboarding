from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):

    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='user_photos')

    def __str__(self):
        return self.username


class Track(models.Model):
    track_name = models.CharField(max_length=50)

    def __str__(self):
        return self.track_name


class Topic(models.Model):
    topic_name = models.CharField(max_length=50)

    def __str__(self):
        return self.topic_name


class Course(models.Model):
    course_name = models.CharField(max_length=50)

    def __str__(self):
        return self.course_name


class Resources(models.Model):
    resource_name = models.CharField(max_length=50)
    resource_cid = models.ForeignKey(Course, on_delete=models.CASCADE)
    resource_descirption = models.TextField()
    resource_link = models.TextField()
    resource_image = models.ImageField(upload_to='resources_photos')

    def __str__(self):
        return self.resource_name