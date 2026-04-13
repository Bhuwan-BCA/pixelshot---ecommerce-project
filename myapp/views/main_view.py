from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from ..models import User
import uuid 
import threading

def send_verification_email(subject, message, recipient):
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient], fail_silently=False)
    except Exception as e:
        print(f"SMTP Error: {e}")

def home_view(request):
    return render(request, 'main/home_page.html')

def password_reset_view(request):
    errors = {}
    if request.method == 'POST':
        email = request.POST.get('email')

        if not email:
            errors['email'] = "Email is required."
        if not User.objects.filter(email=email).exists():
            errors['email'] = "No account found with that email address."

        try:
            user= User.objects.get(email=email)
            reset_token = str(uuid.uuid4())
            user.auth_token = reset_token
            user.save()

            reset_link = f"http://localhost:8000/password-reset/{reset_token}/"   

            subject = "Password Reset Request"
            message = f"Hi {user.first_name},\n\nYou requested a password reset. Click the link below to reset your password:\n{reset_link}\n\nIf you didn't request this, please ignore this email."
            threading.Thread(target=send_mail, args=(subject, message, settings.EMAIL_HOST_USER, [user.email])).start()

            messages.success(request, "Password reset link has been sent to your email.")
            return redirect('/login/')
        
        except User.DoesNotExist:
            messages.error(request, "No account found with that email address.")

        return render(request, 'main/password_reset_page.html', {'errors': errors})
    return render(request, 'main/password_reset_page.html')