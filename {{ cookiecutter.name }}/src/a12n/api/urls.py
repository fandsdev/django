from django.urls import path
from rest_framework_simplejwt import views as jwt

from a12n.api import views


app_name = "a12n"

urlpatterns = [
    path("token/", views.TokenObtainPairView.as_view(), name="auth_obtain_pair"),
    path("token/refresh/", views.TokenRefreshView.as_view(), name="auth_refresh"),
    path("logout/", jwt.TokenBlacklistView.as_view(), name="auth_logout"),
    path("password/change/", views.PasswordChangeView.as_view(), name="auth_change_password"),
]
