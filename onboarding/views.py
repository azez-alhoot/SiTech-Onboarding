from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import Track, Topic, Course, Resources

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