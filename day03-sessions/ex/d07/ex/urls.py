from django.urls import path
from . import views


urlpatterns = [
    path("", views.ex, name="ex"),
    path("username/", views.get_username, name="get_username"),
]
