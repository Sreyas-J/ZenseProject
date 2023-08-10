from django.contrib import admin
from django.urls import path
from . import views

urlpatterns=[
    path('',views.loginPage,name='login'),
    path('home/',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('<str:group>/',views.lobby,name='lobby'),
    path('room/<str:group>/',views.room,name='room'),
    path('<str:group>/get_token/',views.Token,name='token'),
]