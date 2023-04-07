from rest_framework.viewsets import ModelViewSet
from drf_yasg.utils import swagger_auto_schema

from . import serializers
from . import models



class AnnouncementViewSet(ModelViewSet):
    queryset = models.Announcement.objects.all()
    serializer_class = serializers.AnnouncementSerializer

    @swagger_auto_schema(tags=['announcements'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['announcements'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(request_body=serializer_class, tags=['announcements'])    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(request_body=serializer_class, tags=['announcements'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(request_body=serializer_class, tags=['announcements'])    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)