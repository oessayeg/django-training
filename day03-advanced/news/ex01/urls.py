from django.urls import path

from .views.logout import LogoutView
from .views.publications import (
    PublicationsView,
    ArticleDetailView,
    ArticleFavoriteView,
)


urlpatterns = [
    path("publications/", PublicationsView.as_view(), name="publications"),
    path(
        "publications/<int:article_id>/detail/",
        ArticleDetailView.as_view(),
        name="article_detail",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "favorite-articles/", ArticleFavoriteView.as_view(), name="favorite_articles"
    ),
]
