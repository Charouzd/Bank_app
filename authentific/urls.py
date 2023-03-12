from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage),
    path('loggin', views.loggin),
    path('register', views.register),
    path('homepage', views.homepage),
]