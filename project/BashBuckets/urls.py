from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analytics', views.analytics, name='analytics'),
    path('api/listFiles', views.listFiles, name='listFiles'),
]
