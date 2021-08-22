from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, UserTrackForm
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import CustomUser, Topic, TopicCourseBridge, Track, Course, Resources, TrackTopicBridge
from django.shortcuts import render, redirect
from django.db import IntegrityError

# Create your views here.

class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class TrackView(ListView):
    model = Track
    template_name = 'tracks.html'


class CourseView(ListView):
    model = Course
    template_name = 'courses.html'

class ResourcesView(ListView):
    model = Resources
    template_name = 'resources.html'

def user_track_view(request, id1, id2):
    if request.method == "POST":
        try: 
          user = CustomUser.objects.get(id=id1)
          track = Track.objects.get(id=id2)
          form = UserTrackForm(request.POST or None)
          if form.is_valid():
            entry = form.save(commit=False)
            entry.user_id = user
            entry.track_id = track
            entry.save()
            return redirect('track', trackid = id2)

        except IntegrityError:
            context = {
                'error':'you alrady in this track'
            }
            return render(request, 'tracks.html', {'context': context})
    else:
        form = UserTrackForm()
    return render(request, 'tracks.html', {'form': form})


def track_topic_view(request, trackid):

    track_topics_entries = TrackTopicBridge.objects.all().filter(track_id = trackid)

    track_topics = []

    for entry in track_topics_entries:
        track_topics.append(Topic.objects.get(topic_name = entry.topic_id))
   
    return render(request, 'track_topics.html', {'track_topics': track_topics})


def topic_course_view(request ,topicid):

    topic_cousres_entries =TopicCourseBridge.objects.all().filter(topic_id =topicid)

    topic_courses =[]

    for entry in topic_cousres_entries:
        topic_courses.append(Course.objects.get(course_name=entry.course_id))

    return render(request, 'topic_course.html' ,{'topic_courses' : topic_courses})    

    


