from django.urls import path
from . import views


urlpatterns = [
    path("display/", views.display, name="display"),
    path("populate/", views.populate, name="populate"),
    path("update/", views.update, name="update"),
]
