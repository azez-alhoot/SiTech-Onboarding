from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import UserTrackBridge, TrackTopicBridge, TopicCourseBridge, Resource, UserProgress
from django.shortcuts import get_object_or_404


def send_email(context):
    data = "Hello"

    html_message = render_to_string(context['template'], 
            {'username':context['username']})

    if 'track' in context:
        html_message = render_to_string(context['template'], 
            {'username':context['username'], 'track':context['track']})

    to_email = context['user_email']

    send_mail('Welcome! ', data, 'sitech.skillhub@gmail.com', 
        [to_email], fail_silently=False, html_message=html_message)


def calculate_progress(userid):

    progress = []

    tracks = UserTrackBridge.objects.filter(user=userid).values_list('track__id', flat=True)
    tracks_user_enrolled = [item for item in tracks]

    for track in tracks_user_enrolled:
        topics_user_enrolled = []
        courses_user_enrolled = []
        resources_user_enrolled = []
        resources_user_finished = []

        topics = TrackTopicBridge.objects.filter(track=track).values_list('topic__id', flat=True)
        topics_user_enrolled = [item for item in topics]


        for topic in topics_user_enrolled:
            courses = TopicCourseBridge.objects.filter(topic=topic).values_list('course__id', flat=True)
            courses_user_enrolled = [item for item in courses]


        for course in courses_user_enrolled:
            resources = Resource.objects.filter(course=course).values_list('id', flat=True)
            resources_user_enrolled = [item for item in resources]


        for resource in resources_user_enrolled:
            resources_done = UserProgress.objects.filter(user=userid, resource_id=resource).values_list('resource_id', flat=True).first()
            if resources_done:
                resources_user_finished.append(resources_done)
           

      
        number_of_resources_user_enrolled = len(resources_user_enrolled)

        number_of_done_user_resources = len(resources_user_finished)

        progress_float = number_of_done_user_resources / number_of_resources_user_enrolled

        progress_percentage = progress_float * 100

        progress.append([track, round(progress_percentage, 3)])

    return progress
