from django.urls import path
from .views import (
    SignupView,
    tracks_view,
    user_track_view,
    track_topic_view,
    topic_course_view,
    profile_view,
    course_resources_view,
    add_track_form,
    add_to_progress_view,
    delete_from_progress_view,
)
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from .views import LoginView, SignupView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('about_us/', TemplateView.as_view(template_name='about_us.html'),name='about_us'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('tracks/', tracks_view, name='tracks'),
    path('track/<int:trackid>/', track_topic_view, name='track'),
    path('topic/<str:track_name>/<int:topicid>/',topic_course_view, name='topic'),
    path('course/<str:track_name>/<str:topic_name>/<int:courseid>/',course_resources_view, name='course'),
    path('usertrackbridge/<int:user_id>/<int:track_id>/',user_track_view, name='user_track_view'),
    path('profile/', profile_view, name='profile'),
    path('profile/<int:pass_edit>/<int:img_edit>/', profile_view, name='pass_change_profile'),
    path('profile/<int:pass_edit>/<int:img_edit>', profile_view, name='img_edit_profile'),
    path('add-track-form/', add_track_form, name='add_track_form'),
    path('edit-track-form/<int:track_id>',add_track_form, name='edit_track_form'),
    path('add_to_progress_view/<int:user_id>/<int:resource_id>/<str:track_name>/<str:topic_name>/<int:courseid>/',add_to_progress_view, name='add_to_progress_view'),
    path('delete_from_progress_view/<int:user_id>/<int:resource_id>/<str:track_name>/<str:topic_name>/<int:courseid>/',delete_from_progress_view, name='delete_from_progress_view'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
