from django.urls import path
from .views import ChooseChatView, ChatView


urlpatterns = [
    path("chat/", ChooseChatView.as_view(), name="choose_chat"),
    path("chat/<str:room_name>/", ChatView.as_view(), name="chat"),
]
