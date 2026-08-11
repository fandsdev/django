from django.db import DatabaseError, connection
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


@extend_schema(exclude=True)  # the endpoint serves docker and load balancers, not clients generating code
@method_decorator(never_cache, name="dispatch")
class HealthCheckView(APIView):
    authentication_classes = []  # token auth queries the database, so a dead one would 500 before the check below runs

    def get(self, request: Request) -> Response:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except DatabaseError:
            return Response({"db": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response({"db": True})
