from django.contrib import admin
from django.urls import path
from . import views

urlpatterns=[
    path('',views.loginPage,name='login'),
    path('home/',views.home,name='home'),
    path('room/',views.room,name='room'),
    path('get_token/',views.Token,name='token'),
    path('signup/',views.signup,name='signup'),
]