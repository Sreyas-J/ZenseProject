from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/doc/(?P<group>\w+)/(?P<doc>\w+)/$', consumers.EditConsumer.as_asgi()),
]
