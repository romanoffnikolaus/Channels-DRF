import os
import django

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
        users = self.room_name.split('_')
        check = models.Room.objects.filter(customer = users[0],seller=users[1]).exists()
        print(self.scope)

        queryset = models.User.objects.filter(Q(id=users[0])|Q(id=users[-1]))
        customer = queryset[0] if str(queryset[0].id) == users[0] else queryset[1]
        seller = queryset[1] if str(queryset[1].id) == users[1] else queryset[0] 
        if not check:
            self.room = models.Room.objects.create(customer = customer, seller=seller)
        else:
            self.room = models.Room.objects.get(customer = customer, seller=seller)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        history = self.room.room_messages.all()
        history_data = list(map(lambda x: f'{x.publishdate}: {x.content}', history))
        for i in history_data:
            self.send(text_data=json.dumps({
            'message': i}))

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
        print(text_data_json)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        models.Message.objects.create(content=message, room = self.room)

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))