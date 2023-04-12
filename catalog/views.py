from rest_framework.generics import ListAPIView
import django_filters 

from .models import Catalog
from .serializers import CatalogSerializer


class CatalogListView(ListAPIView):
    queryset = Catalog.objects.filter(verified_adress=True).select_related('user')
    serializer_class = CatalogSerializer
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['adress_type']
