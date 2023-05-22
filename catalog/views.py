from rest_framework.generics import ListAPIView
import django_filters 
from rest_framework import filters

from .models import Catalog
from .serializers import CatalogSerializer


class CatalogListView(ListAPIView):
    queryset = Catalog.objects.filter(verified_adress=True).select_related('user')
    serializer_class = CatalogSerializer
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
        ]
    search_fields = ['title', 'description']
    filterset_fields = ['adress_type', 'location']
    ordering_fields = ['rating']

    
    

