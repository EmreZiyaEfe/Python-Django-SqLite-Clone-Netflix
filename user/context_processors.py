from .models import *

def get_profiles(request):
    # if request.user.is_authenticated:
    #     profiller = Profile.objects.filter(user = request.user)
    # else:
    #     profiller=''
    # profiller = Profile.objects.filter(user = request.user)
    profiller = Profile.objects.filter(user = request.user) if request.user.is_authenticated else ''

    context = {
        'profiller' : profiller
    }
    return context