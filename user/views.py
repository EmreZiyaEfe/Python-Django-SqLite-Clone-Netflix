from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def userRegister(request):
    if request.method == 'POST':
        kullanici = request.POST['kullanici']
        email = request.POST['email']
        resim = request.FILES['resim']
        telefon = request.POST['telefon']
        sifre = request.POST['sifre']
        sifre2 = request.POST['sifre2']

        if sifre == sifre2:
            #Kullanıcı adı daha önce kullanılmış mı?
            if User.objects.filter(username = kullanici).exists():
                messages.error(request, 'Kullanıcı Adı mevcut')
            #Email daha önce kullanılmış mı
            elif User.objects.filter(email = email).exists():
                messages.error(request, 'Email Kullanılıyor')
            # Şİfre uzunuğu
            elif len(sifre) < 6:
                messages.error(request, 'Şifre en az 6 Karakter olmalıdır')
            # Şifre ile kullanıcı adı benzer mi?
            elif kullanici.lower() in sifre.lower():
                messages.error(request, 'Kullanıcı adı ile şifre benzer olmamalıdır')
            else:
                user = User.objects.create_user(
                    username = kullanici,
                    email = email,
                    password = sifre
                )
                Hesap.objects.create(
                    user = user,
                    resim = resim,
                    telefon = telefon
                )
                user.save()
                messages.success(request, 'Kayıt yapıldı, Giriş yapabilirsiniz')
                return redirect('index')
        else:
            messages.error(request, 'Şifreler eşleşmedi')
    return render(request, 'register.html')

def userLogin(request):
    if request.method == 'POST':
        kullanici = request.POST['kullanici']
        sifre = request.POST['sifre']

        user = authenticate(request, username = kullanici, password = sifre)

        if user is not None:
            login(request, user)
            messages.success(request, 'Giriş Yapıldı')
            return redirect('profiles')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı')
            return redirect('login')
    return render(request, 'login.html')


# Profil oluşturma  sayfasına ulaşıması için kullanıcının girişli olmasını sağlayan özellik
@login_required(login_url='login') #kullanıcı girişli değilse nereye yönlendireceğini gösterir
def profiles(request):
    profiller = Profile.objects.filter(user = request.user)
    context = {
        'profiller' : profiller
    }
    return render(request, 'browse.html', context)


@login_required(login_url='login')
def create_profile(request):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            if Profile.objects.filter(user = request.user).count() < 4:
                newProfile = form.save(commit=False)
                newProfile.user = request.user
                newProfile.save()
                messages.success(request, 'Profil Oluşturuldu')
                return redirect('profiles')
            else:
                messages.warning(request, 'En fazla 4 adet profil oluşturabilirsiniz')
                return redirect('profiles')
    context = {
        'form':form
    }
    return render(request, 'create-profile.html', context)


def hesap(request):
    profil = request.user.hesap
    context = {
        'profil' : profil
    }
    return render(request, 'hesap.html', context)


def changePassword(request):
    if request.method == 'POST':
        eski = request.POST['eski']
        yeni = request.POST['yeni']
        yeni2 = request.POST['yeni2']

        user = authenticate(request, username = request.user, password = eski)

        if user is not None:
            if yeni == yeni2:
                # istenilen ek şartlar burada if olarak yazılabilir
                user.set_password(yeni)
                user.save()
                messages.success(request, 'Şifreniz değiştirildi')
                return redirect('login')
            else:
                messages.error(request, 'Şifreler uyuşmuyor')
        else:
            messages.error(request, 'Mevcut şifreniz hatalı')

    return render(request, 'change-password.html')



def update(request):
    userForm = UserForm(instance = request.user)
    hesapForm = HesapForm(instance = request.user.hesap)
    if request.method == 'POST':
        userForm = UserForm(request.POST, instance = request.user)
        hesapForm = HesapForm(request.POST, request.FILES, instance = request.user.hesap)
        if userForm.is_valid() and hesapForm.is_valid():
            userForm.save()
            hesapForm.save()
            messages.success(request, 'Bilgiler güncellendi')
            return redirect('hesap')

    context = {
        'user' : userForm,
        'hesap' : hesapForm
    }
    return render(request, 'update.html', context)


def userLogout(request):
    logout(request)
    messages.success(request, 'Çıkıs yapıldı')
    return redirect('index')