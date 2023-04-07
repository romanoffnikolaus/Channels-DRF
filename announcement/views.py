from rest_framework.viewsets import ModelViewSet

from . import serializers
from . import models



class AnnouncementViewSet(ModelViewSet):
    queryset = models.Announcement.objects.all()
    serializer_class = serializers.AnnouncementSerializer