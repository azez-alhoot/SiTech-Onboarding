from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, UserTrackForm
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import CustomUser, Track, Topic, Course, Resources
from django.shortcuts import render, redirect

# Create your views here.


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class TrackView(ListView):
    model = Track
    template_name = 'tracks.html'


class TopicView(ListView):
    model = Topic
    template_name = 'topics.html'


class CourseView(ListView):
    model = Course
    template_name = 'courses.html'

class ResourcesView(ListView):
    model = Resources
    template_name = 'resources.html'

def user_track_view(request, id1, id2):
    if request.method == "POST":
        user = CustomUser.objects.get(id=id1)
        track = Track.objects.get(id=id2)
        form = UserTrackForm(request.POST or None)
        print(form)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user_id = user
            entry.track_id = track
            entry.save()
            return redirect('home')
    else:
        form = UserTrackForm()
    return render(request, 'tracks.html', {'form': form})