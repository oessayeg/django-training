from django.urls import path
from . import views


urlpatterns = [
    path("", views.ex, name="ex"),
    path("login/", views.login, name="login"),
    path("registration/", views.registration, name="registration"),
    path("logout/", views.logout, name="logout"),
]
