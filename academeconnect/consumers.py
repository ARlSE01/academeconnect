from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "chat_room"

        # Add user to the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name  # Correct attribute
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Remove user from the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name  # Correct attribute
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data.get('username','Anonymous')

        # Send message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        await self.send(text_data=json.dumps({'message': message, 'username': username}))