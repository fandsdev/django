from rest_framework.viewsets import ModelViewSet

from sepulkas.api import serializers
from sepulkas.models import Sepulka


class SepulkaViewSet(ModelViewSet):
    serializer_class = serializers.SepulkaSerializer
    serializer_action_classes = {
        'create': serializers.SepulkaCreateSerializer,
        'update': serializers.SepulkaUpdateSerializer,
        'partial_update': serializers.SepulkaUpdateSerializer,
    }
    queryset = Sepulka.objects.all()
