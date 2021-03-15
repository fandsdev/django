from rest_framework import serializers

from sepulkas.models import Sepulka


class SepulkaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sepulka
        fields = [
            'title',
            'cover_image',
        ]


class SepulkaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sepulka
        fields = [
            'title',
            'cover_image',
        ]


class SepulkaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sepulka
        fields = [
            'id',
            'title',
            'cover_image',
        ]
