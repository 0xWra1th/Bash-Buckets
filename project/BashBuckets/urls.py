from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analytics', views.analytics, name='analytics'),
    path('api/listFiles', views.listFiles, name='listFiles'),
    path('api/uploadFile', views.uploadFile, name='uploadFile'),
    path('api/deleteFile', views.deleteFile, name='deleteFile'),
    path('api/deleteFolder', views.deleteFolder, name='deleteFolder'),
    path('api/deleteBucket', views.deleteBucket, name='deleteBucket'),
    path('api/deleteToken', views.deleteToken, name='deleteToken'),
    path('api/createFolder', views.createFolder, name='createFolder'),
    path('api/createBucket', views.createBucket, name='createBucket'),
    path('api/createToken', views.createToken, name='createToken'),
    path('api/listBuckets', views.listBuckets, name='listBuckets'),
    path('api/listTokens', views.listTokens, name='listTokens'),
    path("api/download", views.download, name='download'),
    path("api/createLink", views.createLink, name='createLink'),
    path("api/remainingQuota", views.remainingQuota, name='remainingQuota'),
]
