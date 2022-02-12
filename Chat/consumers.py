import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import MessageModel


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.room_name = None

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        # await self.send(json.dumps({
        #     'by': 'Admin',
        #     'message': 'Welcome ' + self.scope['user'].username,
        # }))

    async def disconnect(self, close_code):
        # Leave room group

        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'by': 'Admin',
        #         'message': self.scope['user'].username + ' disconnected...'
        #     }
        # )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        room_name = text_data_json['roomName']
        sender_id = int(text_data_json['senderId'])
        sender_username = text_data_json['senderUsername']
        receiver_id = int(text_data_json['receiverId'])

        await database_sync_to_async(MessageModel.objects.create)(message=message, room_name=room_name, sender_id=sender_id, receiver_id=receiver_id)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'by': sender_username,
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'by': event['by'],
            'message': event['message'],
        }))
