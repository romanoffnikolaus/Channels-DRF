from rest_framework import serializers
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()


class AnnouncePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnnouncementPhoto
        fields = ('id', 'image', 'announcement')


class AnnouncementSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source='user.id')
    photos = AnnouncePhotoSerializer(many=True, read_only=True)

    class Meta:
        model = models.Announcement
        fields = '__all__'