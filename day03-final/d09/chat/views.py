from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory

from chat.models import ChatRoom, Message


class ChooseChatView(LoginRequiredMixin, ListView):
    model = ChatRoom
    login_url = reverse_lazy("account")
    template_name = "chat/choose_chat.html"


class ChatView(LoginRequiredMixin, FormView):
    form_class = modelform_factory(Message, fields=["content"])
    login_url = reverse_lazy("account")
    template_name = "chat/chat.html"

    def get(self, request, *args, **kwargs):
        room_name = kwargs.get("room_name")
        does_room_exist = ChatRoom.objects.filter(name=room_name).exists()
        if not does_room_exist:
            raise Http404("Room does not exist")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["room_name"] = self.kwargs.get("room_name")
        return context
