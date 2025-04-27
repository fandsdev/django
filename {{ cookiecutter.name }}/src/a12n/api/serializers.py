from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TokenObtainPairWithProperMessageSerializer(TokenObtainPairSerializer):
    default_error_messages = {"no_active_account": _("Invalid username or password.")}


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, style={"input_type": "password"})
    new_password = serializers.CharField(max_length=128, style={"input_type": "password"})
