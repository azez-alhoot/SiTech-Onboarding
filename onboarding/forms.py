from crispy_forms.layout import HTML, Div, Layout, Submit
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import models, formset_factory, BaseFormSet
from django import forms
from .models import CustomUser, Track, UserTrackBridge, UserProgress, Profile, Project
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from django.utils.translation import gettext_lazy as _
import re
# from django.forms import formset_factory

class CustomUserCreationForm(UserCreationForm):
    title = forms.CharField(label='Title')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'example@sitech.me'

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if re.match('\w+(\.)*\w+@(sitech.me|sit-mena.com)', email) != None:
            return email
        raise forms.ValidationError('email should be sitech email', code='adsa')

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('title', 'image')


class CustomUserChangeForm(UserChangeForm):

    title = forms.CharField(label='Title')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].initial = self.instance.profile.title

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name',)


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True
        self.helper.form_id = 'login-form'
        self.helper.form_class = 'uniForm'
        self.helper.form_method = 'POST'
        self.helper.form_action = 'login'

        self.helper.layout = Layout(

            Div('username', css_class='form-group'),
            Div('password', css_class='form-group'),
            Div(
                Submit('submit', 'Login', css_class='btn-custom'),
                css_class='form-group float-end'
                )
        )


class UserTrackForm(models.ModelForm):
    class Meta:
        model = UserTrackBridge
        fields = ('user', 'track')


class EditImageForm(forms.ModelForm):
    image = forms.ImageField(label='', widget=forms.FileInput,required=False)
    class Meta:
        model = Profile
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
        name = self.cleaned_data.get('name')

        if '1' in name:
            raise forms.ValidationError('name cant contain integers', code='adsa')
        return self.cleaned_data

    class Meta:
        model = Track
        fields = '__all__'


class UserProgressForm(models.ModelForm):
    class Meta:
        model = UserProgress
        fields = '__all__'


class AddProjectForm(forms.ModelForm):
        
    class Meta:
        model = Project
        exclude = ['members']
        fields = '__all__'
        # fields = ['name']
        # widgets = {
        #     'name': forms.TextInput(attrs={
        #         'id': 'post-name', 
        #         'required': True, 
        #         'placeholder': 'Say something...'
        #     }),
        # }

class AddProjectMembersForm(forms.Form):

    member_position = forms.CharField(label='member_position', max_length=66)
    member_name = forms.CharField(label='member_name', max_length=66)
    member_linkedIn = forms.CharField(label='member_linkedIn', max_length=66)

