from django.urls import path
from .views import SignupView, TrackView, CourseView, ResourcesView, user_track_view, track_topic_view , topic_course_view
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name = 'home.html'), name = 'home'),
    path('signup/', SignupView.as_view(), name = 'signup'),
    path('tracks/', TrackView.as_view(), name = 'tracks'),
    path('track/<int:trackid>/', track_topic_view, name = 'track'),
    path('topic/<int:topicid>/', topic_course_view, name = 'topic'),
    path('courses/', CourseView.as_view(), name = 'courses'),
    path('resources/', ResourcesView.as_view(), name = 'resources'),
    path('usertrackbridge/<int:id1>/<int:id2>', user_track_view, name = 'user_track_view'),
    
]
