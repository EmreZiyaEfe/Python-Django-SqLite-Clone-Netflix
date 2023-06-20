from django.shortcuts import render
from .models import *
from user.models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def movies(request, profilId, slug):
    profil = Profile.objects.get(id = profilId, slug = slug)
    populer = Movie.objects.filter(kategori__isim = 'Popüler')
    gundem = Movie.objects.filter(kategori__isim = 'Gündemde')
    context = {
        'populer' : populer,
        'gundem' : gundem,
        'profil' : profil,
    }
    return render(request, 'browse-index.html', context)


def video(request, movieId):
    film = Movie.objects.get(id = movieId)
    context = {
        'film' : film
    }
    return render(request, 'video.html', context)

