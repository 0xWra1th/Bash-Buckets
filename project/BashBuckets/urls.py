from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analytics', views.analytics, name='analytics'),
    path('api/listFiles', views.listFiles, name='listFiles'),
    path('api/uploadFile', views.uploadFile, name='uploadFile'),
    path('api/deleteFile', views.deleteFile, name='deleteFile'),
    path('api/createFolder', views.createFolder, name='createFolder'),
    path('api/createBucket', views.createBucket, name='createBucket'),
    path('api/createToken', views.createToken, name='createToken'),
]
