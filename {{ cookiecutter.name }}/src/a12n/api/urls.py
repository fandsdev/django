from django.urls import path

from a12n.api import views


app_name = "a12n"

urlpatterns = [
    path("token/", views.TokenObtainPairView.as_view(), name="auth_obtain_pair"),
    path("token/refresh/", views.TokenRefreshView.as_view(), name="auth_refresh"),
]
