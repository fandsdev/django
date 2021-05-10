from rest_framework.routers import SimpleRouter

from django.urls import include
from django.urls import path

from sepulkas.api import viewsets

router = SimpleRouter()
router.register('', viewsets.SepulkaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
