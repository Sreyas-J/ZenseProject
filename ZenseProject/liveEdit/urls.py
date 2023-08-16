from django.contrib import admin
from django.urls import path
from . import views

urlpatterns=[
    path('<str:group>/<str:doc>/',views.doc,name='doc'),
]