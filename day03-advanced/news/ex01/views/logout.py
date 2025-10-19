from django.views.generic.base import RedirectView
from django.urls import reverse_lazy
from django.contrib.auth import logout


class LogoutView(RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
