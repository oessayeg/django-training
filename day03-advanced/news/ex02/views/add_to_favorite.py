from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.forms import HiddenInput
from django.shortcuts import redirect
from core.models import UserFavoriteArticle


class AddToFavoriteView(LoginRequiredMixin, CreateView):
    model = UserFavoriteArticle
    fields = ["article"]
    success_url = reverse_lazy("publications")
    login_url = "login"

    def get(self, request, *args, **kwargs):
        article_id = self.kwargs.get('article_id')
        return redirect('article_detail', article_id=article_id)

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
        form.instance.user = self.request.user
        article_id = self.kwargs.get('article_id')
        
        if UserFavoriteArticle.objects.filter(user=self.request.user, article_id=article_id).exists():
            messages.warning(self.request, "This article is already in your favorites.")
            return redirect('article_detail', article_id=article_id)
        
        return super().form_valid(form)
