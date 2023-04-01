from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect,reverse
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from Product.models import *
from .models import Profile
import audioop
import os
from django.db.models import Sum




# Create your views here.
def Home(request):
    user = request.user
    if user.is_authenticated:
        cart_items = Cart.objects.filter(user=user)
        cart_total = cart_items.aggregate(total=Sum('subtotal'))['total'] or 0
        cart_obj = Cart.objects.filter(user=user)
        cart_len = len(cart_obj)
    else:
        cart_len = 0
        cart_total = 0
    cat_id = request.GET.get('cat_id')
    search = request.GET.get('search')
    if cat_id:
       p = Product.objects.filter(Catagory=cat_id)
    elif search:
        p = Product.objects.filter(name__icontains=search)
    else:
        p = Product.objects.all()
    c = Catagory.objects.all()
    return render(request, 'home.html', locals())



# registration page work

def register_profile(request):
    if request.method == 'POST':
        name = request.POST['name']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        address_line2 = request.POST['address_line2']
        city_town = request.POST['city_town']
        postcode_zip = request.POST['postcode_zip']
        phone_number = request.POST['phone_number']
        age = request.POST['age']
        gender = request.POST['gender']
        nid_number = request.POST.get('nid_number')
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        additional_information = request.POST['additional_information']

        if password == password1:
            if len(password) < 8 or len(password) > 10:
                messages.info(request, 'Password should be 8-10 characters long. Please insert a valid password.')
                return redirect(reverse('register_profile', args=[]))

            if User.objects.filter(username=name).exists():
                messages.info(request, 'Username already exists. Please use another name.')
                return redirect(reverse('register_profile', args=[]))

            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email address is already taken. Please use another email address.')
                return redirect(reverse('register_profile', args=[]))

            else:
                user = User.objects.create_user(username=name, first_name=first_name, last_name=last_name,
                                                email=email, password=password)
                profile = Profile.objects.create(user=user, address=address, address_line2=address_line2,
                                                  city_town=city_town,
                                                  postcode_zip=postcode_zip, phone_number=phone_number, age=age,
                                                  gender=gender,
                                                  nid_number=nid_number,
                                                  additional_information=additional_information)
                messages.success(request, 'Your registration is successful. Please login.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect(reverse('register_profile'))

    return render(request, 'Registreation.html')

# login page work
def login_page(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        user = auth.authenticate(username=name, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User name or Password not match.')
            return redirect('login')
    return render(request, 'login.html')

# logout_page work
def log_out(request):
    logout(request)
    return redirect('login')

# if login then user can access profile, that's why we use @login_required
@login_required(login_url='login')
def profile_page(request):
    return render(request, 'profile_page.html')

# forgotten password
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
                messages.success(request, 'Reset password is successful')
                return redirect('login')

            else:
                messages.error(request, 'Email not match.')
                return redirect('forgot')
    return render(request,'forget_pass.html')


def bigprof(request):
    user = request.user
    cart_len = 0
    orders = []

    if user.is_authenticated:
        cart_obj = Cart.objects.filter(user=user)
        cart_len = len(cart_obj)
        orders = Order.objects.filter(user=request.user)

    context = {
        'user': user,
        'cart_len': cart_len,
        'orders': orders,
    }
    return render(request, 'profile_page.html', context)


def About(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')
