from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.add_transaction),
    path("dashboard/", views.dashboard),
]