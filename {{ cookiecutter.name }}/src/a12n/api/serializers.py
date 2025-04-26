from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TokenObtainPairWithProperMessageSerializer(TokenObtainPairSerializer):
    default_error_messages = {"no_active_account": _("Invalid username or password.")}
