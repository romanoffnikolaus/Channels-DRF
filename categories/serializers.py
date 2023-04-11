from rest_framework import serializers
from django.contrib.auth import get_user_model

from . models import Category


User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    
    class Meta:
        model = Category
        fields = "__all__"