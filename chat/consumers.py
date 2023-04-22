import os
import django
import channels.auth

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from . import models
from django.db.models import Q



class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        room_data = self.room_name.split('_')
        check = models.Room.objects.filter(customer = room_data[0], announcement=room_data[1]).exists()
        customer = models.User.objects.get(id=room_data[0])
        announcement = models.Announcement.objects.get(slug=room_data[1])
        if not check:
            self.room = models.Room.objects.create(customer = customer, announcement=announcement)
        else:
            self.room = models.Room.objects.get(customer=customer, announcement=announcement)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print(self.__dict__)

        self.accept()
        history = self.room.room_messages.all()
        history_data = [
            {'date': message.publishdate,
             'name': message.author.first_name,
             'id': str(message.author.id),
             'text': message.content
            }
            for message in history
        ]
        # for i in history_data:
        self.send(text_data=json.dumps({
            'messages': history_data}))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = models.User.objects.get(id=text_data_json['author_id'])
        
        message =models.Message.objects.create(content=message, room = self.room, author=user)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {   
                'type': 'chat_message',
                'message': message.content,
                'date': str(message.publishdate),
                'user_name': user.first_name,
                'user_id': str(user.id)
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = {
            'date': event['date'],
            'name': event['user_name'],
            'id': event['user_id'],
            'text': event['message']
        }

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'messages': [message],
        }))