from django.urls import path

from apps.users.api import viewsets

app_name = "users"

urlpatterns = [
    path("me/", viewsets.SelfView.as_view()),
]