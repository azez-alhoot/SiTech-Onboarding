from django.urls import path
from .views import SignUp, Track
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name = 'home.html'), name = 'home'),
    path('signup/', SignUp.as_view(), name = 'signup'),
    path('tracks/', Track.as_view(), name = 'tracks'),
]