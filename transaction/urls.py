from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path("transfer",views.transfer,name='transfer'),
    path("donate",views.donate,name='donate'),
    path("history",views.history,name="history"),
    path("newCourse",views.course,name="course")
]