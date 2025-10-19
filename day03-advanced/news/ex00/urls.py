from django.urls import path
from .views.home import HomeView
from .views.articles import ArticlesView
from .views.login import LoginView


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("articles/", ArticlesView.as_view(), name="articles"),
    path("login/", LoginView.as_view(), name="login"),
]
