from django.urls import re_path
from . import consumers

websocket_urlpatterns=[
    re_path(r'ws/doc/',consumers.EditConsumer.as_asgi())
]