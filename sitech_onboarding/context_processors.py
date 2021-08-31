from onboarding.models import Track

def get_first_track(request):

    return {'track_obj': request.META.get('PATH_INFO', None)}
