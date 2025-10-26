import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chat.models import ChatRoom, Message


class AuthenticatedWebSocketMixin:
    def is_authenticated(self):
        return self.scope["user"].is_authenticated

    def send_auth_error(self, message="Authentication required"):
        self.send(
            text_data=json.dumps(
                {"type": "error", "message": message, "error_code": "AUTH_REQUIRED"}
            )
        )

    def require_authentication(self):
        if not self.is_authenticated():
            self.send_auth_error()
            return False
        return True


class ChatConsumer(AuthenticatedWebSocketMixin, WebsocketConsumer):
    def connect(self):
        if not self.require_authentication():
            self.close()
            return

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat-{self.room_name.replace(' ', '-')}"
        self.chat_room = ChatRoom.objects.get(name=self.room_name)

        messages_history = list(
            Message.objects.filter(chat_room=self.chat_room).order_by("-created_at")[:3]
        )[::-1]

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        self.send(
            text_data=json.dumps(
                {
                    "type": "messages_history",
                    "messages": [
                        {
                            "user": message.user.username,
                            "message": message.content,
                            "type": "message",
                        }
                        for message in messages_history
                    ],
                }
            )
        )
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "join_message",
                "user": self.scope["user"].username,
                "message": f"{self.scope['user'].username} has joined the chat",
            },
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        # Check authentication before processing message
        if not self.require_authentication():
            return

        text_data_json = json.loads(text_data)
        message = text_data_json.get("message", "")
        username = self.scope["user"].username
        chat_room = self.chat_room.name
        messageInstance = Message(
            content=message, user_id=username, chat_room_id=chat_room
        )
        messageInstance.save()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "user": username,
                "message": message,
            },
        )

    def chat_message(self, event):
        self.send(
            text_data=json.dumps(
                {
                    "type": "message",
                    "user": event["user"],
                    "message": event["message"],
                }
            )
        )

    def join_message(self, event):
        self.send(
            text_data=json.dumps(
                {
                    "type": "join_message",
                    "message": event["message"],
                }
            )
        )
