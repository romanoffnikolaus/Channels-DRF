from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
import django_filters
from rest_framework import filters

from . import serializers
from . import models
from . import permissions as prm
from review.models import Favorite
from review.serializers import CommentSerializer


class PermissionsMixin():
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = [AllowAny]
        elif self.action in ['create']:
            permissions = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy', ]:
            permissions = [prm.IsOwnerOrReadOnly]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]


class AnnouncementViewSet(PermissionsMixin, ModelViewSet):
    queryset = models.Announcement.objects.all()
    serializer_class = serializers.AnnouncementSerializer
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter]
    search_fields = ['title', 'description']
    filterset_fields = ['title', 'location', 'category', 'price']
    ordering_fields = ['created_at', 'price', 'views_count', 'rating']
    ordering = ['created_at']
    parser_classes = [MultiPartParser]
    
    @swagger_auto_schema(tags=['announcements'])
    def list(self, request, *args, **kwargs):
        lower_price =self.request.query_params.get('lower_price')
        higher_price =self.request.query_params.get('higher_price')
        queryset = self.filter_queryset(self.get_queryset())
        if lower_price and higher_price:
            queryset = queryset.filter(price__range=(lower_price, higher_price))
        elif lower_price and not higher_price:
            queryset = queryset.filter(price__range=(lower_price, 1000000))
        elif not lower_price and higher_price:
            queryset = queryset.filter(price__range=(lower_price, higher_price))
        serializer = self.get_serializer(queryset, many=True)
        for i in range(len(queryset)):
            photos = queryset[i].announcementImages.all()
            serializer.data[i]['photos'] = serializers.AnnouncePhotoSerializer(photos, many=True).data
        return Response(serializer.data)
    
    @action(['POST'], detail=True)
    def comment(self, request, pk=None):
        self.permission_classes = [IsAuthenticated]
        announcement = self.get_object()
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(announsment=announcement)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    @swagger_auto_schema(tags=['announcements'])
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1 
        instance.save()
        serializer = self.get_serializer(instance)
        announsment_photos = instance.announcementImages.all()
        announsment_photo_serializer = serializers.AnnouncePhotoSerializer(announsment_photos, many=True)
        response_data = {**serializer.data, 'photos': announsment_photo_serializer.data}
        comments = instance.comment.all()
        comment_serializer = CommentSerializer(comments, many=True)
        response_data['comments'] = comment_serializer.data
        return Response(response_data)

    @swagger_auto_schema(request_body=serializer_class, tags=['announcements'])    
    def create(self, request, *args, **kwargs):
        photos = request.FILES.getlist('photos')
        data = request.data.copy()
        data.pop('photos', None)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        announcement = serializer.save(user=self.request.user)
        images = [models.AnnouncementPhoto(announcement=announcement, image=image) for image in photos]
        models.AnnouncementPhoto.objects.bulk_create(images)
        return Response(serializer.data, status=201)
    
    @swagger_auto_schema(request_body=serializer_class, tags=['announcements'])
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        images = request.FILES.getlist('photos')
        data = request.data.copy()
        data.pop('photos', None)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if images:
            models.AnnouncementPhoto.objects.filter(announcement=instance).delete()
            announcement_photos = [models.AnnouncementPhoto(announcement=instance, image=image) for image in images]
            models.AnnouncementPhoto.objects.bulk_create(announcement_photos)
        response_data = serializer.data
        report_images = instance.announcementImages.all()
        announsment_photo_serializer = serializers.AnnouncePhotoSerializer(report_images, many=True)
        response_data['photos'] = announsment_photo_serializer.data
        return Response(response_data)
    
    @swagger_auto_schema(request_body=serializer_class, tags=['announcements'])    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @action(['POST'], detail=True)
    def favorite(self, request, pk):
        self.permission_classes = [IsAuthenticated]
        announcement = self.get_object()
        user = request.user
        try:
            favorite = Favorite.objects.get(announcement=announcement, user=user)
            favorite.is_favorite = not favorite.is_favorite
            favorite.save()
            message = 'Объявление добавлено в избранное' if favorite.is_favorite else 'Объявление удалено из избранного'
            if not favorite.is_favorite:
                favorite.delete()
        except Favorite.DoesNotExist:
            Favorite.objects.create(
                announcement=announcement, user=user, is_favorite=True)
            message = 'Объявление добавлено в избранноое'
        return Response(message, status=200)
