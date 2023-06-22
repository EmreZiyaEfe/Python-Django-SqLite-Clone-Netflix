from django.urls import path
from .views import *

urlpatterns = [
    path('register/', userRegister, name='register'),
    path('login/', userLogin, name='login'),
    path('logout/', userLogout, name='logout'),
    path('profiles/', profiles, name='profiles'),
    path('create-profile/', create_profile, name='create'),
    path('hesap/', hesap, name='hesap'),
    path('change-password/', changePassword, name='change'),
    path('update/', update, name='update')

]