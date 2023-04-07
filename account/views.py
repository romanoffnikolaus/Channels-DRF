from django.contrib.auth import get_user_model
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema

import serializers

User = get_user_model()

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.Profileserializer

    @swagger_auto_schema(request_body=serializer_class, tags=['account'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(request_body=serializer_class, tags=['account'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(request_body=serializer_class, tags=['account'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(request_body=serializer_class, tags=['account'])    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(request_body=serializer_class, tags=['account'])    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


