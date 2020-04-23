from django.urls import path

from users.api import views

app_name = 'users'
urlpatterns = [
    path('me/', views.SelfView.as_view()),
]
