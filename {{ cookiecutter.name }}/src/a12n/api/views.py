from rest_framework_simplejwt import views as jwt

from a12n.api.throttling import AuthAnonRateThrottle


class TokenObtainPairView(jwt.TokenObtainPairView):
    throttle_classes = [AuthAnonRateThrottle]


class TokenRefreshView(jwt.TokenRefreshView):
    throttle_classes = [AuthAnonRateThrottle]
