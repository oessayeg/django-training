from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from core.models import Article


class PublishView(LoginRequiredMixin, CreateView):
    template_name = "ex02/publish.html"
    model = Article
    fields = ["title", "synopsis", "content"]
    success_url = reverse_lazy("publications")
    login_url = "login"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
