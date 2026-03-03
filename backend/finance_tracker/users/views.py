from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from finance.services import set_initial_balance
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.hashers import make_password
from .models import PasswordResetCode
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
import random
from django.contrib.auth import authenticate
from django_ratelimit.decorators import ratelimit


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
@ratelimit(key="post:email", rate="3/m", block=True)
def forgot_password(request):
    email = request.data.get("email")

    if not email:
        return Response({"error": "Email required"}, status=400)

    try:
        user = User.objects.get(email=email)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"http://localhost:5173/reset-password/{uid}/{token}/"

        code = str(random.randint(100000, 999999))

        PasswordResetCode.objects.filter(user=user).delete

        PasswordResetCode.objects.create(
            user=user,
            code=code
        )

        send_mail(
            subject="Reset your password",
            message=(
                f"Click this link:\n{reset_link}\n\n"
                f"Your verification code is:{code}\n\n"
                "This code expires in 5 minutes."
                ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response({"message": "reset email sent"})

    except User.DoesNotExist:
        return Response({"error": "Email not registered"}, status=404)
    

@api_view(["POST"])
def reset_password(request):
    uid = request.data.get("uid")
    token = request.data.get("token")
    code = request.data.get("code")
    new_password = request.data.get("password")
    email = request.data.get("email")

    if not all([uid, token, code, new_password, email]):
        return Response({"error": "All fields required"}, status=400)
    
    
    try:
        user_id = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=user_id)

        if user.email != email:
            return Response({"error": "Invalid email"}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired link"}, status=400)

        reset_obj = PasswordResetCode.objects.get(user=user, code=code)

        if reset_obj.is_expired():
            reset_obj.delete()
            return Response({"error": "Code expired"}, status=400)

        user.password = make_password(new_password)
        user.save()

        reset_obj.delete()

        return Response({"message": "Password reset successful"})

    except PasswordResetCode.DoesNotExist:
        return Response({"error": "invalid code"}, status=400)

    except Exception:
        return Response({"error": "Invalid request"}, status=400)

@api_view(["POST"])
def verify_reset_code(request):
    email = request.data.get("email")
    code = request.data.get("code")

    try:
        user = User.objects.get(email=email)
        reset_obj = PasswordResetCode.objects.get(user=user, code=code)
        
        if reset_obj.is_expired():
            reset_obj.delete()
            return Response({"error": "Code expired"}, status=400)

        return Response({"verified": True})

    except:
        return Response({"error": "Invalid code"}, status=400)

