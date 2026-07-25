from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from app.api.healthchecks import HealthCheckView


app_name = "api_v1"

urlpatterns = [
    path("auth/", include("a12n.api.urls")),
    path("users/", include("users.api.urls")),
    path("healthchecks/", HealthCheckView.as_view(), name="healthchecks"),
    path("docs/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema")),
]
