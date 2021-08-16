from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.views.generic.edit import CreateView

# Create your views here.


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'onboarding/signup.html'
