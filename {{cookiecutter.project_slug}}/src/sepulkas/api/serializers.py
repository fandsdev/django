from rest_framework import serializers

from sepulkas.models import Sepulka


class SepulkaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sepulka
        fields = [
            'id',
            'name',
            'description',
            'created',
            'modified',
        ]


class SepulkaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sepulka
        fields = [
            'id',
            'name',
            'description',
        ]


class SepulkaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sepulka
        fields = [
            'id',
            'description',  # Can only update description
        ]
