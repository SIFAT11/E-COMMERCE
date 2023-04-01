from django.urls import path
from .views import *

urlpatterns = [
    path('', Home, name='home'),
    path('log/', login_page, name='login'),
    path('log_out/', log_out, name='logout'),
    path('reg/', register_profile, name='Registreation'),
    path('About/', About, name='about'),
    path('contact/', contact, name='contact'),
    path('pro/',profile_page , name='pro_page'),
    path('big_pro/', bigprof, name='pro_big'),
    path('fpass/', forgot, name='forgot'),
]
