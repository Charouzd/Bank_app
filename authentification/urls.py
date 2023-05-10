
from django.contrib import admin
from django.urls import include, path
from authentification import views

urlpatterns = [
    path('', views.home,name="home"),
    path("signup",views.sign_up,name='signup'),
    path("signin",views.sign_in,name='signin'),
    path("signout",views.sign_out,name='signout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path("test",views.testing,name="nothing"),
    path("resetTest",views.testingOUT,name="donenothing"),
]
