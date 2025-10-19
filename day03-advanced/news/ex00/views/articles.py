from django.views.generic import ListView

from core.models import Article


class ArticlesView(ListView):
    model = Article
    template_name = "ex00/articles.html"
