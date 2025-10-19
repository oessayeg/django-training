from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.forms import HiddenInput
from core.models import UserFavoriteArticle


class AddToFavoriteView(CreateView):
    model = UserFavoriteArticle
    fields = ["article"]
    success_url = reverse_lazy("publications")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['article'].widget = HiddenInput()
        return form

    def get_initial(self):
        initial = super().get_initial()
        article_id = self.kwargs.get('article_id')
        if article_id:
            initial['article'] = article_id
        return initial

    def form_valid(self, form):
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("Please login to add an article to your favorites")
        form.instance.user = user
        return super().form_valid(form)
