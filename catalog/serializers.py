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
        fields = ('__all__')

    def validate_rating(self, rating):
        if rating < 1 and rating > 5:
            raise serializers.ValidationError(
                'Значение рейтинга должно быть от 1 до 5'
            )
        return rating