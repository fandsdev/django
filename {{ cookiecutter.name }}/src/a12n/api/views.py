from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import views as jwt
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken

from a12n.api.serializers import PasswordChangeSerializer
from a12n.api.throttling import AuthAnonRateThrottle
from app.api.request import AuthenticatedRequest
from users.models import User


class TokenObtainPairView(jwt.TokenObtainPairView):
    throttle_classes = [AuthAnonRateThrottle]


class TokenRefreshView(jwt.TokenRefreshView):
    throttle_classes = [AuthAnonRateThrottle]


class PasswordChangeView(APIView):
    """Change user password, invalidate active user refresh tokens and return new token pair."""

    throttle_classes = [AuthAnonRateThrottle]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=PasswordChangeSerializer,
        responses=inline_serializer("PasswordChangeResponse", {"refresh": serializers.CharField(), "access": serializers.CharField()}),
    )
    def post(self, request: AuthenticatedRequest) -> Response:
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.validate_and_change_password(
            user=request.user,
            old_password=serializer.validated_data["old_password"],
            new_password=serializer.validated_data["new_password"],
        )
        self.blacklist_active_user_tokens(request.user)

        refresh = RefreshToken.for_user(request.user)
        return Response({"refresh": str(refresh), "access": str(refresh.access_token)})

    def validate_and_change_password(self, user: User, old_password: str, new_password: str) -> None:
        """Change password with django's change password form or raise serializer aware field errors."""
        form = PasswordChangeForm(user=user, data={"old_password": old_password, "new_password1": new_password, "new_password2": new_password})

        if not form.is_valid():
            if "new_password2" in form.errors:
                form.errors["new_password"] = form.errors.pop("new_password2")  # to raise matched error fields matched serializer
            raise serializers.ValidationError(form.errors)  # type: ignore[arg-type]

        form.save()

    def blacklist_active_user_tokens(self, user: User) -> None:
        """Blacklist all active refresh tokens and force other user devices to relogin."""
        active_tokens = OutstandingToken.objects.filter(user=user, blacklistedtoken__isnull=True, expires_at__gt=timezone.now())

        BlacklistedToken.objects.bulk_create(
            [BlacklistedToken(token=token, blacklisted_at=timezone.now()) for token in active_tokens],
        )
