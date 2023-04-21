from rest_framework import serializers

from . models import Room, Announcement


class YourChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class Roomserializer(serializers.ModelSerializer):
    rooms = serializers.SerializerMethodField()
    class Meta:
        model = Announcement
        fields = ['rooms', 'slug']

    def get_rooms(self, instance):
        rooms = instance.rooms.all()
        data = YourChatsSerializer(rooms, many=True).data
        return data
