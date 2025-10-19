from django.views.generic import ListView

from ex00.models import Article


class ArticlesView(ListView):
    model = Article
    template_name = "ex00/articles.html"
