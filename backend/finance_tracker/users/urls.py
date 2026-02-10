from django.urls import path
from .views import signup, login, forgot_password, reset_password

urlpatterns = [
    path("signup/", signup),
    path("login/", login),
    path("forgot-password", forgot_password),
    path("reset-password", reset_password),
]