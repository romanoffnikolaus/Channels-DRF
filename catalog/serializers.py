from rest_framework import serializers

from . models import Catalog


class CatalogSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    class Meta:
        model = Catalog
        fields = ('adress', 'adress_type', 'user', 'id')