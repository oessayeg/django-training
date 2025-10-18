from django.urls import path
from . import views


urlpatterns = [
    path("", views.ex, name="ex"),
    path("login/", views.login, name="login"),
    path("registration/", views.registration, name="registration"),
    path("logout/", views.logout, name="logout"),
    path("tip/<int:tip_id>/action/", views.tip_action, name="tip_action"),
    path("api/anonymous-username/", views.get_anonymous_username, name="get_anonymous_username"),
]
