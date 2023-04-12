from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from .serializers import NewsSerializer
from .models import News


class NewsView(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny,]
        else: 
            self.permission_classes = [IsAdminUser,]
        return super().get_permissions()


