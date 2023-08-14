from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('doc/',include('liveEdit.urls')),
    path('',include('videoCall.urls')),
]
