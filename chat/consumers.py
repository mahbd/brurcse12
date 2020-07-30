import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message
from home.all_functions import last_message_update, get_name


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']
        sender = await get_user(sender_id)
        recipient_id = text_data_json['recipient_id']
        await last_message_for_here(sender, recipient_id, message)
        mess_obj = await save_message(sender_id, message, recipient_id)
        date = mess_obj.sent_at
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
                'recipient_id': recipient_id,
                'date': date,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        recipient_id = event['recipient_id']
        date = event['date']
        user = self.scope['user']
        name = await user_name_by_user_id(sender_id)
        if user.id != sender_id:
            message = '<div class="col-auto"><p class="btn-primary rounded"><small>' + name + ' ' + date.strftime("%a %I:%M %p") + '</small><br>' + message + '</div><div class="col"></div>'
        else:
            message = '<div class="col"></div><div class="ml-md-auto"><p class="btn-success rounded"><small>' + name + ' ' + date.strftime("%a %I:%M %p") + '</small><br>' + message + '</div>'

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender_id,
            'recipient_id': recipient_id,
        }))


@database_sync_to_async
def get_user(user_id):
    return User.objects.get(id=user_id)


@database_sync_to_async
def save_message(sender_id, message, recipient_id):
    print(sender_id, recipient_id)
    mess_obj = Message(sender_id=sender_id, message=message, recipient_id=recipient_id)
    mess_obj.save()
    return mess_obj


@database_sync_to_async
def last_message_for_here(sender, recipient_id, message):
    print(recipient_id)
    last_message_update(sender, recipient_id, message)


@database_sync_to_async
def user_name_by_user_id(user_id):
    print(user_id)
    user = User.objects.get(id=user_id)
    name = get_name(user)
    return name
