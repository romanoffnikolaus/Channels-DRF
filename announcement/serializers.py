from rest_framework import serializers
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()


class AnnouncePhotoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = models.AnnouncementPhoto
        fields = ('id', 'image', 'announcement', 'image_url')
    
    def get_image_url(self, obj): #Изменить URL перед деплоем. Это костыль.
        if obj.image:
            return f'https://enactusanimals.com/media/{obj.image.name}'
        return None



class AnnouncementSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source='user.id')
    photos = AnnouncePhotoSerializer(many=True, read_only=True)

    class Meta:
        model = models.Announcement
        fields = '__all__'