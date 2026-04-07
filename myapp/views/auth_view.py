from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from ..models import User
import uuid 
import threading


def register_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return render('/')
    

    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        profile_picture = request.FILES.get('profile_picture')  # Handle profile picture upload 
        auth_token = str(uuid.uuid4()) 
        
        
        
        if not username:
            errors['username']= "Username is required." 
        if User.objects.filter(username=username).exists():
            errors['username']= "Username already exists." 
        
        if not first_name:
            errors['first_name']= "First name is required."
        if not last_name:
            errors['last_name']= "Last name is required."

        if not email:
            errors['email']= "Email is required."
        if User.objects.filter(email=email).exists():
            errors['email']= "Email already registered."

        if not password:
            errors['password']= "Password is required."
        if password != confirm_password:
            errors['confirm_password']= "Passwords do not match."

        
        if not errors:
            user = User.objects.create_user(
                username=username,
                email=email, 
                password=password, 
                first_name=first_name, 
                last_name=last_name, 
                profile_picture=profile_picture, 
                auth_token=auth_token
            )
            user.save()

            verify_url = f"http://127.0.0.1:8000/verify/{auth_token}/"
            subject = "Welcome to PixelShot - Verify Your Email"
            message = f"Hi {first_name},\n\nWelcometo PixelShot!\n\nPlease verify your email by clicking the link below:\n\n{verify_url}\n\nBest regards,\nThe PixelShot Team"

            threading.Thread(target=send_verification_email, args=(subject, message, email)).start()
            messages.success(request, "Registration successful! Please check your email to verify your account.")
            return redirect('/login/')
        
        return render(request, 'auth/register_page.html', {'data': request.POST, 'errors': errors})
    return render(request, 'auth/register_page.html')
       


def login_view(request):
    return render(request, 'auth/login_page.html')

def send_verification_email(subject, message, recipient):
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient], fail_silently=False)
    except Exception as e:
        print(f"SMTP Error: {e}")

