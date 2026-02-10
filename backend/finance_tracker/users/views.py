from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from finance.services import set_initial_balance
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
import random
from django.contrib.auth import authenticate

RESET_CODES = {}

@api_view(["POST"])
def signup(request):
    email = (request.data.get("email") or "").strip()
    username = (request.data.get("username") or "").strip()
    password = request.data.get("password")
    balance = request.data.get("balance")

    if not email or not username or not password:
        return Response({"error": "All fields required"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)
    
    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered"}, status=400)
    
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    if balance:
        try:
            set_initial_balance(user.id, float(balance))
        except:
            pass
    return Response({"message": "Signup successful"})

@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=400)
    
    user = authenticate(request, username=user_obj.username, password=password)

    if not user:
        return Response({"error": "Invalid credentials"}, status=400)
    
    refresh = RefreshToken.for_user(user)


    return Response({
        "access": str(refresh.access_token), 
        "refresh": str(refresh),
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    })

@api_view(["POST"])
def forgot_password(request):
    email = request.data.get("email")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Email not registered"}, status=400)
    
    code = str(random.randint(100000, 999999))
    RESET_CODES[email] = {
        "code": code,
        "expires": timezone.now() + timedelta(minutes=5)
    }

    send_mail(
        subject="Your Password Reset Code",
        message=f"Your reset code is: {code}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return Response({"message": "Reset code sent"})

@api_view(["POST"])
def reset_password(request):
    email = request.data.get("email")
    code = request.data.get("code")
    new_password = request.data.get("password")

    if email not in RESET_CODES:
        return Response({"error": "No reset request found"}, status=400)
    
    data = RESET_CODES[email]

    if datetime.utcnow() > data["expires"]:
        del RESET_CODES[email]
        return Response({"error": "Reset code expired"}, status=400)
    if data["code"] != code:
        return Response({"error": "Invalid code"}, status=400)
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=400)
    
    user.password = make_password(new_password)
    user.save()

    del RESET_CODES[email]

    return Response({"message": "Password reset successful"})