from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework_jwt import views as jwt

from django.utils.decorators import method_decorator

from a12n.api.throttling import AuthAnonRateThrottle

USER_RESPONSE = openapi.Response(
    description='User id and token',
    schema=openapi.Schema(
        type='array',
        items=[
            openapi.Schema(title='id', type='string', description='User id'),
            openapi.Schema(title='token', type='string', description='JWT Token'),
        ]),
)


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_id='Obtain JWT Token',
    operation_description='Exchange valid username and password pair to the JWT token',
    responses={
        200: USER_RESPONSE,
    },
))
class ObtainJSONWebTokenView(jwt.ObtainJSONWebTokenView):
    throttle_classes = [AuthAnonRateThrottle]


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_id='Refresh JWT Token',
    responses={
        200: USER_RESPONSE,
    },
))
class RefreshJSONWebTokenView(jwt.RefreshJSONWebTokenView):
    throttle_classes = [AuthAnonRateThrottle]
