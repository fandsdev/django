from django.db.models import QuerySet
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.api.request import AuthenticatedRequest
from users.api.serializers import UserSerializer
from users.models import User


class SelfView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    request: AuthenticatedRequest

    def get(self, request: AuthenticatedRequest) -> Response:
        user = self.get_object()
        serializer = self.get_serializer(user)

        return Response(serializer.data)

    def get_object(self) -> User:
        return self.get_queryset().get(pk=self.request.user.pk)

    def get_queryset(self) -> QuerySet[User]:
        return User.objects.filter(is_active=True)
