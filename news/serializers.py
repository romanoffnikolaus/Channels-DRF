from rest_framework import serializers

from .models import News


class NewsSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = News
        fields = '__all__'