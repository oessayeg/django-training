from django.core.exceptions import PermissionDenied
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from core.models import Article


class PublishView(CreateView):
    template_name = "ex02/publish.html"
    model = Article
    fields = ["title", "synopsis", "content"]
    success_url = reverse_lazy("publications")

    def form_valid(self, form):
        author = self.request.user
        if not author.is_authenticated:
            raise PermissionDenied("Please login to publish an article")
        form.instance.author = author
        return super().form_valid(form)
