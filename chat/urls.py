# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:customer>/<str:seller>/', views.room, name='room'),
    path('your_chats/', views.YourChatListView.as_view()),
    # path('seller_chats/', views.SellerChatsListView.as_view()),
]