# chat/views.py
from django.shortcuts import render
import django.core.handlers.asgi
from rest_framework import generics
from rest_framework.response import Response

from .models import Room, Message, Announcement
from .serializers import YourChatsSerializer, Roomserializer


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
        return Response(data, 200)
    
