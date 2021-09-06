from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_email(context):
    data = "Hello"

    html_message = render_to_string(context['template'], 
            {'username':context['username']})

    if 'track' in context:
        html_message = render_to_string(context['template'], 
            {'username':context['username'], 'track':context['track']})

    to_email = context['user_email']

    send_mail('Welcome! ', data, 'sitech.skillhub@gmail.com', 
        [to_email], fail_silently=False, html_message=html_message)