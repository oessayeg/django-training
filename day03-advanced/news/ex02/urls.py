from django.urls import path

from ex02.views.publish import PublishView
from ex02.views.registration import RegistrationView
from ex02.views.add_to_favorite import AddToFavoriteView

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("publish/", PublishView.as_view(), name="publish"),
    path("add-to-favorite/<int:article_id>/", AddToFavoriteView.as_view(), name="add_to_favorite"),
]
