from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


# Create your views here.
def Home(request):
    return render(request, 'home.html')


# registration from work
def Regis(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if password == password1:
            if User.objects.filter(username=name).exists():  # filter  to cheak function
                messages.info(request, 'Username already exists.Please use another name.')
                return redirect('Registreation')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email are already taken.Please use another Email address.')
                return redirect('Registreation')

            else:
                user = User.objects.create_user(username=name, email=email, password=password)
                user.set_password(password)
                user.save()
                messages.success(request, 'Your registration is successful.Please Login')
            return redirect('login')
        else:
            messages.error(request, 'Password not same.')
            return redirect('Registreation')
    return render(request, 'Registreation.html')


# login page work
def login_page(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        user = auth.authenticate(username=name, password=password)
        if user:
            login(request, user)  # if name match thenb it works
        else:
            messages.error(request, 'User name or Password not match.')
            return redirect('login')  # if not mathch it back in the login page
        return redirect('home')
    return render(request, 'login.html')


# logout_page work
def log_out(request):
    logout(request)
    return redirect('login')


# lf login then user can access profile thats why we use @login requre
@login_required(login_url='login')
def Profile_page(request):
    return render(request, 'profile_page.html')


# forgottenb password.if user forgot password then use it
def forgot(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['new_pass']

        if name != None:
            user = User.objects.get(username=name)
            if user.email == email:
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'reset password_Update is successful')
                return redirect('login')

            else:
                messages.error(request, 'Email not match.')
                return redirect('forgot')

    return render(request, 'forget_pass.html')


def bigprof(request):
    return render(request, 'BIGProf.html')


def About(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')
