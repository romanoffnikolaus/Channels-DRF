from rest_framework.viewsets import ModelViewSet
from drf_yasg.utils import swagger_auto_schema
from . models import Category
from . import serializers


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

    @swagger_auto_schema(tags=['categories'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=['categories'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(request_body=serializer_class, tags=['categories'])    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(request_body=serializer_class, tags=['categories'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(request_body=serializer_class, tags=['categories'])    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
