from app.viewsets import AppViewSet
from sepulkas.api import serializers
from sepulkas.models import Sepulka


class SepulkaViewSet(AppViewSet):
    serializer_class = serializers.SepulkaSerializer  # Detail
    serializer_action_classes = {
        'create': serializers.SepulkaCreateSerializer,
        'update': serializers.SepulkaUpdateSerializer,
        'partial_update': serializers.SepulkaUpdateSerializer,
    }
    queryset = Sepulka.objects.all()
