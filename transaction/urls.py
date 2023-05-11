from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path("transfer",views.transfer,name='transfer'),
    path("recieve",views.recieve,name='recieve'),
    path("send",views.send,name='send'),
]