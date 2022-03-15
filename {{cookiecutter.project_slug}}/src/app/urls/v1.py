from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView

from django.urls import include
from django.urls import path

app_name = 'api_v1'
urlpatterns = [
    path('auth/', include('a12n.urls')),
    path('users/', include('users.urls')),
    path('healthchecks/', include('django_healthchecks.urls')),
    path('docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema')),
]
