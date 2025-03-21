from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
import json
from chatapp.models import ChatGroup, GroupMessage
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup,group_name=self.chatroom_name)

        async_to_sync(self.channel_layer.group_add) (
            self.chatroom_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        body = data['body']

        message = GroupMessage.objects.create(
            body=body,
            author=self.user,
            group=self.chatroom
        )

        event={
            'type': 'message_handler',
            'message_id': message.id,
        }

        async_to_sync(self.channel_layer.group_send)(self.chatroom_name,event)

    def message_handler(self, event):
        message_id=event['message_id']
        message =GroupMessage.objects.get(id=message_id)
        context = {
            'message': message,
            'user': self.user,
        }
        html = render_to_string("chatapp/partials/chat_message_p.html", context)
        self.send(text_data=html)


