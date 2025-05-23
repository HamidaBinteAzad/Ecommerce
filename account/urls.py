from django.urls import path
from .views import *

urlpatterns = [
    path("registration/", registration, name='registration'),
    path("login/", user_login, name='login'),
    path("logout/", user_logout, name='logout'),
    path("verify-otp/", verify_otp, name='verify_otp'), 
    path("forget_password/", forget_password, name='forget_password'), 
    path("verify_forget_pass/", verify_forget_pass, name='verify_forget_pass'),
    path("user_dashboard/", user_dashboard, name='user_dashboard'),
    path("update_profile/<int:id>/", update_profile, name='update_profile'),
]
