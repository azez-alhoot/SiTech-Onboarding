from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Track(models.Model):
    track_name = models.CharField(max_length=50)  

    def __str__(self):
        return self.track_name

class CustomUser(AbstractUser):


    track_objects = Track.objects.values_list('track_name', flat=True)

    tracks = []

    for object in track_objects:
        tracks.append((object,f'{object}'))


    title = models.CharField(max_length=50, default='Software Engineer', choices=tracks)
    image = models.ImageField(upload_to='static/user_photos/')

    

    def __str__(self):
        return self.username





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

class UserTrackBridge(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    track_id = models.ForeignKey(Track, on_delete=models.CASCADE, blank=True)

    class Meta:
        unique_together = ('user_id', 'track_id')

    def __str__(self):
        return f'user => {self.user_id} , track => {self.track_id}'


class TrackTopicBridge(models.Model):
    track_id = models.ForeignKey(Track, on_delete=models.CASCADE, blank=True)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f'track => {self.track_id}, topic => {self.topic_id}'

class TopicCourseBridge(models.Model):
    topic_id=models.ForeignKey(Topic,on_delete=models.CASCADE,blank=True)  
    course_id=models.ForeignKey(Course,on_delete=models.CASCADE,blank=True)    

    def __str__(self):
        return f'topic=> {self.topic_id} , course => {self.course_id}'