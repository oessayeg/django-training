from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView
from core.models import Article


class PublicationsView(ListView):
    model = Article
    template_name = "ex01/publications.html"

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Article.objects.filter(author=user).all()
        raise PermissionDenied("Please login to view your publications")


class ArticleDetailView(DetailView):
    model = Article
    template_name = "ex01/details.html"
    context_object_name = "article"
    pk_url_kwarg = "article_id"


class ArticleFavoriteView(ListView):
    model = Article
    template_name = "ex01/favourite_articles.html"

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            return Article.objects.filter(userfavoritearticle__user=user)
        raise PermissionDenied("Please login to view your favourite articles")
