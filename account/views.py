from django.shortcuts import render, redirect, HttpResponseRedirect
from . models import Custom_User
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
import random
from django.contrib import messages



# Create your views here.

# def registration(request):
#     return render(request, 'auth/registration.html')

def registration(request):
    if request.user.is_authenticated:
        messages.success(request, "You are Already Logged In.")
        return redirect('home')
    

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip_code')
        image = request.FILES.get('image')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            otp = random.randint(1000, 9999)
            user = Custom_User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, phone=phone, address=address, city=city, state=state, country=country, zip_code=zip_code, image=image, otp=otp, password=password1 )
            user.save()
            send_email(email, otp)
            return redirect('verify_otp')

    return render(request, 'auth/login.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_verified:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "Please verify your account first.")
                return redirect('verify_otp')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'auth/login.html')  # Return login page on failure

    # Handle GET request (render login page)
    return render(request, 'auth/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')


def send_email(email, otp):
    subject = 'Welcome to our website'
    message = f'Thank you for registering with us your otp is {otp}.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp:
            user = Custom_User.objects.filter(otp=otp).first()
            if user:
                user.is_verified = True
                user.save()
                return redirect('registration')
            else:
                return redirect('verify_otp')
    return render(request, 'auth/otp_submit.html')


def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = Custom_User.objects.filter(email=email).first()
        if user:
            otp = random.randint(1000, 9999)
            user.otp = otp
            user.save()
            send_email(email, otp)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, "Email not found.")

    return render(request, 'auth/forget_page.html')

def verify_forget_pass(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if otp and password1 and password2:
            user = Custom_User.objects.filter(otp=otp).first()
            if user:
                if password1 == password2:
                    user.set_password(password1)
                    user.save()
                    return redirect('login')
                else:
                    messages.error(request, "Password did not match.")
            else:
                messages.error(request, "Invalid OTP.")
    return redirect('login')


# def user_dashboard(request):
#     if not request.user.is_verified:
#         return redirect('registration')
#     else:
#         if request.user.is_verified:
#             user = request.user
#             user_data = Custom_User.objects.get(id= user.id)

#     return render(request, 'auth/user_dashboard.html', {'user_data': user_data})

# updated code

def user_dashboard(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Check if user is verified
    if not request.user.is_verified:
        return redirect('registration')
    
    # Use request.user directly; no need to query the database again
    user_data = request.user
    
    return render(request, 'auth/user_dashboard.html', {'user_data': user_data})


# def update_profile(request, id):
#     user = Custom_User.objects.get(id=id)
#     if request.method == 'POST':
#         user.first_name = request.POST.get('first_name')
#         user.last_name = request.POST.get('last_name')
#         user.email = request.POST.get('email')
#         password = request.POST.get('password')
#         if password:
#             user.set_password(password)  # Correctly set the hashed password
#         user.save()
#         # Consider logging the user back in after password change to maintain session
#         return redirect('user_dashboard')  # Use redirect instead of HTTP_REFERER for better control
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404


@login_required(login_url='login')
def update_profile(request, id):
    user = get_object_or_404(Custom_User, id=id)

    # Ensure user can only update their own profile
    if request.user.id != user.id:
        messages.error(request, "You can only update your own profile.")
        return redirect('user_dashboard')

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        
        password = request.POST.get('password')
        if password:
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)  # ✅ Keeps the user logged in after password change
        else:
            user.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('user_dashboard')

    return render(request, 'auth/edit_profile.html', {'user': user})






