from django.urls import path,include
from rest_framework import routers
from . import views




urlpatterns = [
    path('', views.HomeViewSet.as_view(), name='home'),
    path('explore/', views.ExploreViewSet.as_view(), name='explore'),
]