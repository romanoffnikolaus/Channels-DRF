from rest_framework import generics
from .models import ForumPost
from django.contrib.auth import get_user_model
from . import serializers

User = get_user_model()

class ForumPostView(generics.CreateAPIView):
    queryset = ForumPost.objects.all()
    serializer_class = serializers.ForumSerializer