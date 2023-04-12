from rest_framework import serializers

from .models import AnnouncementComment
from announcement.serializers import AnnouncementSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    announsment = AnnouncementSerializer(read_only=True, source='announcement')

    class Meta:
        model = AnnouncementComment
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        comment = AnnouncementComment.objects.create(user=user, **validated_data)
        return comment

    