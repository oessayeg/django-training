from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView
from django.forms import HiddenInput
from core.models import Article, UserFavoriteArticle
from django.forms import ModelForm

class PublicationsView(ListView):
    model = Article
    template_name = "ex01/publications.html"

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Article.objects.filter(author=user).order_by('-created').all()
        raise PermissionDenied("Please login to view your publications")


class ArticleDetailView(DetailView):
    model = Article
    template_name = "ex01/details.html"
    context_object_name = "article"
    pk_url_kwarg = "article_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        class AddToFavoriteForm(ModelForm):
            class Meta:
                model = UserFavoriteArticle
                fields = ['article']
                widgets = {
                    'article': HiddenInput()
                }
        
        form = AddToFavoriteForm(initial={'article': self.object.id})
        context['form'] = form
        return context


class ArticleFavoriteView(ListView):
    model = Article
    template_name = "ex01/favourite_articles.html"

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            return Article.objects.filter(userfavoritearticle__user=user).order_by('-created').all()
        raise PermissionDenied("Please login to view your favourite articles")
