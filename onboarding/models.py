# from typing_extensions import Required
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver



class Track(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.FileField(upload_to='tracks_photos', validators=[FileExtensionValidator(['png', 'jpg', 'svg'])])

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='user_photos/', default='default_avatar.png', blank=True)

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=CustomUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return str(self.title) or "N/A"


class Topic(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.FileField(upload_to='topics_photos', validators=[FileExtensionValidator(['png', 'jpg', 'svg'])])

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.FileField(upload_to='courses_photos', validators=[FileExtensionValidator(['png', 'jpg', 'svg'])])
    prerequisite = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Resource(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField()
    link = models.TextField()
    image = models.FileField(upload_to='resources_photos', validators=[FileExtensionValidator(['png', 'jpg', 'svg'])])

    def __str__(self):
        return self.name


class UserTrackBridge(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, blank=True)
    progress = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('user', 'track')

    def __str__(self):
        return f'user: {self.user}, track: {self.track}'


class TrackTopicBridge(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f'track: {self.track}, topic: {self.topic}'


class TopicCourseBridge(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f'topic: {self.topic}, course: {self.course}'


class UserProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, blank=True)

    class Meta:
        unique_together = ('user', 'resource')

    def __str__(self):
        return f'user: {self.user}, resource: {self.resource}'

class Project(models.Model):
    name = models.CharField(max_length=66)
    description = models.TextField()
    members = models.JSONField()
    business_document =models.FileField()
    technical_document =models.FileField()

    def __str__(self):
        return self.name