from django.urls import include, path

app_name = 'api_v1'
urlpatterns = [
    path('healthchecks/', include('django_healthchecks.urls')),
]
