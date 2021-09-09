from onboarding.models import Track, UserProgress

def get_first_track(request):

    return {'track_obj': request.META.get('PATH_INFO', None)}

def get_user_progress(request):
    user = request.user.id
    progress = UserProgress.objects.filter(user=user).values_list('resource__id',flat=True).distinct()
    return {'progress':progress}