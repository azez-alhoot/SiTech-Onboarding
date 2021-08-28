from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, UserTrackForm, CustomUserChangeForm
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import CustomUser, Topic, TopicCourseBridge, Track, Course, Resource, TrackTopicBridge, UserTrackBridge
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

# Create your views here.


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class TrackView(ListView):
    model = Track
    template_name = 'tracks.html'



def user_track_view(request, user_id, track_id):
    if request.method == "POST":
        entry = UserTrackBridge.objects.filter(user=user_id, track=track_id)
        if not entry:
            user = CustomUser.objects.get(id=user_id)
            track = Track.objects.get(id=track_id)
            form = UserTrackForm(request.POST or None)
            if form.is_valid():
                entry = form.save(commit=False)
                entry.user = user
                entry.track = track
                entry.save()
                return redirect('track', trackid=track_id)
        else:
            return redirect('track', trackid=track_id)
    else:
        form = UserTrackForm()
    return render(request, 'tracks.html', {'form': form})


def track_topic_view(request, trackid):

    topics = TrackTopicBridge.objects.filter(track=trackid).values_list('topic_id', 'topic__name', 'topic__descirption', 'topic__image')

    return render(request, 'track_topics.html', {'topics': topics})


def topic_course_view(request, topicid):

    courses = TopicCourseBridge.objects.filter(topic=topicid).values_list('course_id', 'course__name', 'course__descirption', 'course__image')

    return render(request, 'topic_courses.html', {'courses': courses})


def course_resources_view(request, courseid):
    resources = Resource.objects.filter(course=courseid).values_list('name', 'descirption', 'image', 'link')

    return render(request, 'course_resources.html', {'resources': resources})


def profile_view(request, userid):
    tracks = UserTrackBridge.objects.filter(user=userid).values_list('track_id','track__name')

    return render(request, 'profile.html', {'tracks': tracks})


def profile_edit_view(request, userid):

    user = CustomUser.objects.get(id=userid)
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', userid=userid)
    else:
        form = CustomUserChangeForm(
            initial={'first_name': user.first_name, 'last_name': user.last_name})

    return render(request, 'profile_edit.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })