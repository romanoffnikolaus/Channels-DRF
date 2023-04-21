# chat/views.py
from django.shortcuts import render
import django.core.handlers.asgi
from rest_framework import generics

from .models import Room
from .serializers import YourChatsSerializer


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
    
    def get_queryset(self):
        return Room.objects.filter(customer=self.request.user.id)