from django.urls import include
from django.urls import path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='{{ cookiecutter.project_slug }} API',
        default_version='v1',
        contact=openapi.Contact(email='{{ cookiecutter.email }}'),
    ),
    public=True,
    permission_classes=[permissions.IsAdminUser],
)


app_name = 'api_v1'
urlpatterns = [
    path('users/', include('users.urls')),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('healthchecks/', include('django_healthchecks.urls')),
]
