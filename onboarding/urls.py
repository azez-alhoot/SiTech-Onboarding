from django.urls import path
from .views import SignUp
from django.views.generic.base import TemplateView

urlpatterns = [
    path('signup/', SignUp.as_view(), name = 'sign_up'),
    path('home/', TemplateView.as_view(template_name='home.html'), name = 'home'),
]