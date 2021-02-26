from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.api.serializers import UserSerializer
from users.models import User


class SelfView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: UserSerializer}, operation_id='whoami', operation_description='Get current user data')
    def get(self, request):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def get_object(self) -> User:
        return self.get_queryset().get(pk=self.request.user.pk)

    def get_queryset(self):
        return User.objects.filter(is_active=True)
