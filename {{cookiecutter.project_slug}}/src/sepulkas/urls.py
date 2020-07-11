from django.urls import include, path
from rest_framework.routers import SimpleRouter

from sepulkas.api import views as sepulkas

router = SimpleRouter()
router.register('', sepulkas.SepulkaViewSet, basename='sepulka')

app_name = 'sepulkas'
urlpatterns = [
    path('', include(router.urls)),
]
