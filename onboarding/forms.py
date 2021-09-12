from crispy_forms.layout import HTML, Div, Layout, Submit
# from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import models
from django import forms
from .models import CustomUser, Track, UserTrackBridge, UserProgress
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'title', 'username', 'email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'title')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email')

class UserTrackForm(models.ModelForm):
    class Meta:
        model = UserTrackBridge
        fields = ('user', 'track')


class EditImageForm(forms.ModelForm):
    image = forms.ImageField(required = False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)

    class Meta:
        model = CustomUser
        fields = ('image',)


class AddTrackForm(models.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag=True
        self.helper.layout = Layout(
            Div(
                Div(
                    'name',
                    css_class='col-5'
                ),
                css_class='row'

            ),
            Div(
                Div(
                    HTML('<h3>Add new Track</h3>'),
                    css_class='col-5'
                ),
                css_class='row'

            ),
            Div(
                Div(
                    'descirption',
                    css_class='col-5'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    'image',
                    css_class='col-5'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    Submit('submit', 'save',
                    css_class='btn-danger'
                    ),
                    css_class='col-5'
                ),
                css_class='row'
            ),

        )

    def clean_name(self):
        name=self.cleaned_data.get('name')

        if '1' in name:
            raise forms.ValidationError('name cant contain integers', code='adsa')
        return self.cleaned_data()

    class Meta:
        model = Track
        fields = '__all__'


class UserProgressForm(models.ModelForm):
    class Meta:
        model = UserProgress
        fields = '__all__'