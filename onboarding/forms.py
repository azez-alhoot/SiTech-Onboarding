from django.contrib.auth import forms
# from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import models
from .models import CustomUser, UserTrackBridge

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','title', 'username', 'email',)
        
    
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'title', 'image',)


class UserTrackForm(models.ModelForm):
    class Meta:
        model = UserTrackBridge
        fields = ('user', 'track')