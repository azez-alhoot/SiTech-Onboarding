from django.db.transaction import commit
from django.forms.formsets import formset_factory
from django.template import context
from django.core import serializers

from .forms import (
    CustomUserCreationForm,
    UserTrackForm,
    CustomUserChangeForm,
    EditImageForm,
    AddTrackForm,
    UserProgressForm,
    LoginForm,
    AddProjectForm,
    AddProjectMembersForm,
)
from .models import (
    CustomUser,
    Project,
    TopicCourseBridge,
    Track,
    Resource,
    TrackTopicBridge,
    UserTrackBridge,
    UserProgress,
    Profile,
)
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash, authenticate
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .helper import send_email, calculate_progress
from django.contrib.auth import views as auth_views
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy
from contextlib import contextmanager

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.forms import formset_factory, modelformset_factory


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, AuthenticationForm):
        title = AuthenticationForm.cleaned_data["title"]
        user = AuthenticationForm.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your blog account.'
        message = render_to_string('registration/welcome-email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.id)),
            'token': account_activation_token.make_token(user),
            'title': title,
        })
        to_email = AuthenticationForm.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        msg = 'Please confirm your email address to complete the registration'
        return render(self.request, 'home.html', {'msg': msg})


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'

    error_messages = {
        'invalid_login': gettext_lazy('Please enter a correct email and password. Note that both fields may be case-sensitive.'),
        'inactive': gettext_lazy("..."),
    }

    def post(self, request, *args, **kwargs):
        with self.handle_msg():
            rtn_response: TemplateResponse = super(
                LoginView, self).post(request, *args, **kwargs)
        return rtn_response

    @contextmanager
    def handle_msg(self):
        org_msg = AuthenticationForm.error_messages
        AuthenticationForm.error_messages = self.error_messages
        try:
            yield self.error_messages
        finally:
            AuthenticationForm.error_messages = org_msg


def tracks_view(request):

    tracks = Track.objects.all()
    user_tracks = UserTrackBridge.objects.filter(
        user=request.user).values_list('track__name', flat=True)
    user_tracks_list = [track for track in user_tracks]

    return render(request, 'tracks.html', {'tracks': tracks, 'user_tracks_list': user_tracks_list})


@login_required
def user_track_view(request, user_id=None, track_id=None):

    if request.method == "POST":
        entry = UserTrackBridge.objects.filter(
            user=user_id, track=track_id).exists()
        if not entry:
            user = CustomUser.objects.get(id=user_id)
            track = Track.objects.get(id=track_id)
            form = UserTrackForm(request.POST or None)
            if form.is_valid():
                entry = form.save(commit=False)
                entry.user = user
                entry.track = track
                entry.save()

                context = {
                    'track': track,
                    'username': request.user.username,
                    'user_email': request.user.email,
                    'template': 'congrats-email.html',
                }
                send_email(context)

                return redirect('tracks')
        else:
            return redirect('tracks')
    else:
        form = UserTrackForm()
    return render(request, 'tracks.html')


def track_topic_view(request, trackid):

    topics = TrackTopicBridge.objects.filter(track=trackid).values_list(
        'topic_id', 'topic__name', 'topic__description', 'topic__image', 'track__name')

    courses_query = TopicCourseBridge.objects.filter().values_list('course__name',
                                                                   'topic__id', 'course__description', 'course__prerequisite', 'course_id')

    courses = [course for course in courses_query]

    return render(request, 'track_topics.html', {'topics': topics, 'courses': courses})


def course_resources_view(request, track_name, topic_name, courseid):
    resources = Resource.objects.filter(course=courseid).values_list(
        'name', 'description', 'image', 'link', 'course__name', 'course__id', 'id')
    track = Track.objects.filter(name=track_name).values_list('id')
    track_id = track[0][0]
    enrolled_tracks = UserTrackBridge.objects.filter(
        user=request.user).values_list('track__name', flat=True)

    return render(request, 'course_resources.html', {'resources': resources, 'track_name': track_name, 'topic_name': topic_name, 'course_id': courseid, 'track_id': track_id, 'course_name': resources[0][4], 'enrolled_tracks': enrolled_tracks})


def profile_view(request, pass_edit=None, img_edit=None):

    userid = request.user.id

    calculate_progress(userid)

    tracks = UserTrackBridge.objects.filter(user=userid).values_list(
        'track_id', 'track__name', 'track__description', 'track__image', 'progress')

    user = CustomUser.objects.get(id=userid)

    form_edit_user = CustomUserChangeForm(request.POST or None, instance=user)

    form_edit_image = EditImageForm(
        request.POST or None, request.FILES or None, instance=user.profile)

    form_change_password = PasswordChangeForm(
        request.user, request.POST or None)

    if form_edit_image.is_valid() and img_edit:
        form_edit_image.save()
        return redirect('profile')

    if form_change_password.is_valid() and pass_edit:
        user = form_change_password.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Your password was successfully updated!')
        return redirect('home')
    else:
        messages.error(request, 'Please correct the error below.')

    if form_edit_user.is_valid():
        form_edit_user.save()
        profile = Profile.objects.get(user=user)
        title = form_edit_user.cleaned_data['title']
        profile.title = title
        profile.save()
        return redirect('profile')

    return render(request, 'profile.html',
                  {'tracks': tracks,
                   'form_edit_user': form_edit_user,
                   'form_edit_image': form_edit_image,
                   'form_change_password': form_change_password})


# this is for learning and practice
def add_track_form(request, track_id=None):
    instance = Track()

    if track_id:
        instance = Track.objects.get(id=track_id)
    
    form = AddTrackForm(request.POST or None, request.FILES or None, instance=instance, user=request.user)

    # print(form)

    if form.is_valid():
        form.save()
        print("*******************************************************")
        print('all good')

    return render(request, 'forms/add-track-form.html', {'form': form})



def add_to_progress_view(request, user_id, resource_id, track_name, topic_name, courseid):

    user = CustomUser.objects.get(id=user_id)
    resource = Resource.objects.get(id=resource_id)

    form = UserProgressForm(request.POST or None)

    if form.is_valid():
        entry = form.save(commit=False)
        entry.user = user
        entry.resource = resource
        entry.save()
        return redirect('course', track_name=track_name, topic_name=topic_name, courseid=courseid)
    else:
        return redirect('course', track_name=track_name, topic_name=topic_name, courseid=courseid)


def delete_from_progress_view(request, user_id, resource_id, track_name, topic_name, courseid):
    user = CustomUser.objects.get(id=user_id)
    resource = Resource.objects.get(id=resource_id)

    UserProgress.objects.filter(user=user, resource=resource).delete()

    return redirect('course', track_name=track_name, topic_name=topic_name, courseid=courseid)


def activate(request, uidb64, token, title):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.title = title
        user.save()
        msg = 'Thank you for your email confirmation. Now you can login your account.'
        form = LoginForm()
        return render(request, 'registration/login.html', {'msg': msg, 'form': form})
    else:
        return HttpResponse('Activation link is invalid!')


def projects_view(request):
    projects = Project.objects.all()

    return render(request, 'projects.html', {'projects': projects})


def projects_details_view(request, project_id):
    project = Project.objects.get(id=project_id)

    return render(request, 'project_details.html', {'project': project})


def add_project_view(request, project_id=None):
    
    instance = AddProjectForm()

    if project_id:
        instance = Project.objects.get(id=project_id)
        members = Project.objects.filter(id=project_id).values_list('members')
        form = AddProjectForm(request.POST or None, instance=instance)
        form_set_t = formset_factory(AddProjectMembersForm, can_delete=True)
        formset = form_set_t(request.POST or None,members)
        print(members)
    else:
        form = AddProjectForm(request.POST or None, request.FILES or None)
        form_set_t = formset_factory(AddProjectMembersForm,extra=1, can_delete=True)
        formset = form_set_t(request.POST or None)

        data = request.POST
        print(data)
        if form.is_valid() and formset.is_valid():
            print('*************************************')
            print('*************************************')
            print('All Good')
            print('*************************************')
            print('*************************************')
            return redirect('projects_view')


    return render(request, 'add_project.html', {'form':form, 'formset':formset})
    return render(request, 'project_details.html', {'project':project})


def dashboard_view(request):
    return render(request, 'admin_dashboard.html')
