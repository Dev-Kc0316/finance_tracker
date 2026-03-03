from django.urls import path
from .views import signup, login, forgot_password, verify_reset_code,reset_password

urlpatterns = [
    path("signup/", signup),
    path("login/", login),
    path("forgot-password/", forgot_password),
    path("verify-reset-code/", verify_reset_code),
    path("reset-password/", reset_password),
]