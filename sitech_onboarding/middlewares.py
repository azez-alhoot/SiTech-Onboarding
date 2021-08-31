import re
from urllib.parse import urlparse

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.mail import mail_managers
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.urls import is_valid_path
from django.urls.base import reverse
from django.utils.deprecation import MiddlewareMixin
from django.utils.http import escape_leading_slashes
from onboarding.models import CustomUser



class CompleteProfile(MiddlewareMixin):

    response_redirect_class = HttpResponsePermanentRedirect

    def process_request(self, request):
        
        url = request.META.get('PATH_INFO', None)
        if request.user.is_authenticated and not (
            request.user.is_staff or request.user.is_superuser
        ):
            if not 'profile' in url:
                profile = CustomUser.objects.get(id=request.user.id)

                if not profile.first_name:

                    return HttpResponseRedirect(reverse('profile'))
