from django.views.generic.edit import FormView
from django.contrib.auth import login
from ex00.forms import LoginForm
from django.urls import reverse_lazy


class LoginView(FormView):
    template_name = "ex00/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("articles")

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

