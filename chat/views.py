# chat/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, customer, seller):
    room_name = customer

    return render(request, 'chat/room.html', {
        # 'room_name': room_name,
        'seller': seller,
        'customer': customer,
    })