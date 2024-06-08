# predictions/urls.py

from django.urls import path
from . import views

urlpatterns = [
     path('weather/', views.get_weather, name='get_weather'),
    # path('weather/<str:location>/<str:plant>/', views.get_weather, name='get_weather'),
]
