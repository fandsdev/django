from django.contrib import admin
from django.urls import include
from django.urls import path

api = [
    path('v1/', include('app.urls.v1', namespace='v1')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api)),
]
