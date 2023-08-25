from django.contrib import admin
from django.urls import path
from . import views

app_name = 'videoCall'

urlpatterns=[
    path('',views.loginPage,name='login'),
    path('home/',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('createGroup/',views.createGroup,name='createGroup'),
    path('<str:group>/',views.lobby,name='lobby'),
    path('room/<str:group>/',views.room,name='room'),
    path('room/<str:group>/addMember/',views.addMember,name='addMember'),
    path('room/<str:group>/addDoc/',views.addDoc,name='addDoc'),
    path('recording/<str:group>/<str:record>/',views.view_recording,name='view recording'),

    path('<str:group>/get_token/',views.Token,name='token'),
    path('create_recording/<str:group>/',views.record,name='recording'),
    path('update_recording/<str:group>/',views.update_record,name='update_recording'),
    path('create_member/',views.createMember,name='createMember'),
]