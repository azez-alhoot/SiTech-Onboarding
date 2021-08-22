from django.contrib.auth.forms import UserCreationForm
from django.forms import models
from .models import CustomUser, UserTrackBridge

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name','title', 'username', 'email',)


class UserTrackForm(models.ModelForm):
    class Meta:
        model = UserTrackBridge
        fields = ('user_id', 'track_id')