from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Track, Topic, Course, Resources
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class Track(ListView):
    model = Track
    template_name = 'tracks.html'


class Topic(ListView):
    model = Topic
    template_name = 'topics.html'


class Course(ListView):
    model = Course
    template_name = 'courses.html'

class Resources(ListView):
    model = Resources
    template_name = 'resources.html'