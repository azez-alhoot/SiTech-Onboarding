from django.urls import reverse_lazy, reverse
from .forms import (
    CustomUserCreationForm, 
    UserTrackForm, 
    CustomUserChangeForm, 
    AddTrackForm,
    )
from django.views.generic.edit import CreateView
from .models import CustomUser, Topic, TopicCourseBridge, Track, Resource, TrackTopicBridge, UserTrackBridge
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash, authenticate
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required



class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, AuthenticationForm):
    
        to_return = super().form_valid(AuthenticationForm)
        user = authenticate(
            username=AuthenticationForm.cleaned_data["username"],
            password=AuthenticationForm.cleaned_data["password1"],
        )
        login(self.request, user)
        return to_return
    

class TrackView(ListView):
    model = Track
    template_name = 'tracks.html'

@login_required
def user_track_view(request, user_id=None, track_id=None):
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

    topics = TrackTopicBridge.objects.filter(track=trackid).values_list('topic_id', 'topic__name', 'topic__descirption', 'topic__image', 'track__name')

    return render(request, 'track_topics.html', {'topics': topics})


def topic_course_view(request, track_name, topicid):
    
    courses = TopicCourseBridge.objects.filter(topic=topicid).values_list('course_id', 'course__name', 'course__descirption', 'course__image', 'topic__name', 'topic__id')
    track = Track.objects.filter(name=track_name).values_list('id')
    track_id = track[0][0]

    return render(request, 'topic_courses.html', {'courses': courses, 'track_name':track_name, 'topic_id':topicid, 'track_id':track_id})


def course_resources_view(request, track_name, topic_name, courseid):
    resources = Resource.objects.filter(course=courseid).values_list('name', 'descirption', 'image', 'link', 'course__name', 'course__id')
    topic = Topic.objects.filter(name=topic_name).values_list('id')
    topic_id = topic[0][0]
    track = Track.objects.filter(name=track_name).values_list('id')
    track_id = track[0][0]
    
    return render(request, 'course_resources.html', {'resources': resources, 'track_name':track_name, 'topic_name':topic_name, 'topic_id':topic_id, 'course_id': courseid, 'track_id':track_id})


def profile_view(request):

    userid = request.user.id

    tracks = UserTrackBridge.objects.filter(user=userid).values_list('track_id','track__name', 'track__descirption', 'track__image')
    
    user = CustomUser.objects.get(id=userid)
    
    form_edit_user = CustomUserChangeForm(request.POST or None, request.FILES or None, instance=user)

    form_change_password = PasswordChangeForm(request.user, request.POST or None)
    
    if form_edit_user.is_valid():
        form_edit_user.save()
        return redirect('profile')

    if form_change_password.is_valid():
        user = form_change_password.save()
        update_session_auth_hash(request, user)  
        messages.success(request, 'Your password was successfully updated!')
        return redirect('home')
    else:
        messages.error(request, 'Please correct the error below.')
        
    
    return render(request, 'profile.html', 
    {'tracks': tracks, 
    'form_edit_user': form_edit_user , 
    'form_change_password':form_change_password})


# this is for learning and practice

def add_track_form(request, track_id=None):
    instance = Track()

    if track_id:
        instance = Track.objects.get(id=track_id)
    
    form = AddTrackForm(request.POST or None, request.FILES or None, instance=instance, user=request.user)

    if form.is_valid():
        form.save()

    return render(request, 'forms/add-track-form.html', locals())