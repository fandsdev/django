from django.urls import include, path

app_name = 'api_v1'
urlpatterns = [
    path('users/', include('users.urls')),
    path('healthchecks/', include('django_healthchecks.urls')),
]
