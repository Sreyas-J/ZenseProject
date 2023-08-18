from django.contrib import admin
from django.urls import path
from . import views

app_name = 'liveEdit'

urlpatterns=[
    path('<str:group>/<str:doc>/',views.doc,name='doc'),
]