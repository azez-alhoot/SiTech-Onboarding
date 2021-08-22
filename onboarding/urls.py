from django.urls import path
from .views import SignupView, TrackView, user_track_view, track_topic_view , topic_course_view, profile_view, profile_edit_view, course_resources_view ,change_password
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name = 'home.html'), name = 'home'),
    path('signup/', SignupView.as_view(), name = 'signup'),
    path('tracks/', TrackView.as_view(), name = 'tracks'),
    path('track/<int:trackid>/', track_topic_view, name = 'track'),
    path('topic/<int:topicid>/', topic_course_view, name = 'topic'),
    path('course/<int:courseid>/', course_resources_view, name = 'course'),
    path('usertrackbridge/<int:id1>/<int:id2>/', user_track_view, name = 'user_track_view'),
    path('profile/<int:userid>/', profile_view, name = 'profile'),
    path('profile/edit/<int:userid>/', profile_edit_view, name = 'profile_edit'),
    path(r'^password/$', change_password, name='change_password'),
    
]
