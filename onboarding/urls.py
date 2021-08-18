from django.urls import path
from .views import SignupView, TrackView, TopicView, CourseView, ResourcesView, user_track_view
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name = 'home.html'), name = 'home'),
    path('signup/', SignupView.as_view(), name = 'signup'),
    path('tracks/', TrackView.as_view(), name = 'tracks'),
    path('topics/', TopicView.as_view(), name = 'topics'),
    path('courses/', CourseView.as_view(), name = 'courses'),
    path('resources/', ResourcesView.as_view(), name = 'resources'),
    path('usertrackbridje/<int:id1>/<int:id2>', user_track_view, name = 'user_track_view'),
]
