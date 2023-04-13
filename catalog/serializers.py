from rest_framework import serializers
from django.contrib.auth import get_user_model

from . models import Catalog


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'image', 'first_name')


class CatalogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Catalog
        fields = ('adress', 'adress_type', 'id','user')
