# chat/views.py
from django.shortcuts import render
import django.core.handlers.asgi
from rest_framework import generics
from rest_framework.response import Response

from .models import Room, Message, Announcement, User
from .serializers import YourChatsSerializer, Roomserializer
from .consumers import domain
from account.serializers import Profileserializer


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, customer, seller):
    room_name = customer


    return render(request, 'chat/room.html', {
        # 'room_name': room_name,
        'seller': seller,
        'customer': customer
    })


class YourChatListView(generics.ListAPIView):
    serializer_class = YourChatsSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        self.queryset = Room.objects.filter(customer=request.user)
        user_announcements = Announcement.objects.filter(user=request.user)
        announcement_rooms = Roomserializer(user_announcements, many=True).data
        rooms_queryset = [room for item in announcement_rooms for room in item['rooms'] ]
        data = super().list(self,request, *args, **kwargs).data + rooms_queryset
        for room_data in data:
            room_id = room_data['id']
            if request.user.id == room_data['customer']:
                other_user = Announcement.objects.get(slug=room_data['announcement']).user
                room_photo = domain + Profileserializer(other_user).data['image']
                if not room_photo:
                    room_photo = None
            else:
                other_user = User.objects.get(id=room_data['customer'])
                room_photo = domain + Profileserializer(other_user).data['image']
                if not room_photo:
                    room_photo = None
            room_data['photo'] = room_photo
            last_message = Message.objects.filter(room_id=room_id).order_by('-date').first()
            if last_message:
                try:
                    author_photo = domain + last_message.author.image.url
                except:
                    author_photo = None
                room_data['last_message'] = {
                    'content': last_message.content,
                    'author': last_message.author.id,
                    'date': last_message.publishdate,
                    'author_name': last_message.author.first_name,  
                    'author_photo': author_photo,             
                }
            else:
                room_data['last_message'] = None
        return Response(data, 200)
    


    
