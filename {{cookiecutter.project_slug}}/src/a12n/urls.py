from django.urls import path

from a12n.api import views

app_name = 'a12n'
urlpatterns = [
    path('token/', views.ObtainJSONWebTokenView.as_view()),
    path('token/refresh/', views.RefreshJSONWebTokenView.as_view()),
]
