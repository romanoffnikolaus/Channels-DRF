from rest_framework import generics
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .models import Favorite
from .serializers import FavoritesSerializer
from announcement.models import Announcement
from .models import ForumPost
from django.contrib.auth import get_user_model
from . import serializers

User = get_user_model()

class ForumPostView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ForumPost.objects.all()
    serializer_class = serializers.ForumSerializer


class FavoritesView(APIView):
    
    @swagger_auto_schema(tags=['favorites'])
    def get(self, request):
        queryset = Favorite.objects.filter(user=request.user)
        serializer = FavoritesSerializer(queryset, many=True)
        return Response(serializer.data, status=200)
    
    @swagger_auto_schema(tags=['favorites'])
    def delete(self, request, pk):
        try:
            favorite = Favorite.objects.get(id=pk)
            favorite.delete()
            return Response(f'Объявление удалено из избранного')

        except Favorite.DoesNotExist:
            return Response("Объявление удалено из избранного")
