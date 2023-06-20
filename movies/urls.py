from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('movies/<profilId>/<slug>', movies, name='movies'),
    path('movies/<movieId>/', video, name='video')
]
