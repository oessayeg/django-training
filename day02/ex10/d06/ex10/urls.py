from django.urls import path
from . import views


urlpatterns = [
    path("", views.ex10, name="ex10"),
]
