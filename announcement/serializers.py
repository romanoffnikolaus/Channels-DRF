from rest_framework import serializers
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()

class AnnouncementSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Announcement
        fields = '__all__'
