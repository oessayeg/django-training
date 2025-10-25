from django.contrib.auth import login, logout
from django.views.generic import FormView, View
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.http import JsonResponse


class AccountView(FormView):
    form_class = AuthenticationForm
    template_name = "account/ex00.html"
    success_url = reverse_lazy("account")

    def form_valid(self, form):
        login(self.request, form.get_user())
        return JsonResponse(
            {"status": "success", "logged_user": form.get_user().get_full_name()}
        )

    def form_invalid(self, form):
        return JsonResponse({"status": "error", "errors": form.errors})


class LogoutView(View):
    def post(self, request):
        logout(request)
        return JsonResponse({"status": "success"})
