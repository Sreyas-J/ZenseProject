from django.urls import re_path
from . import consumers

<<<<<<< HEAD
websocket_urlpatterns=[
    re_path(r'ws/doc/',consumers.EditConsumer.as_asgi())
]
=======
websocket_urlpatterns = [
    re_path(r'ws/doc/(?P<group>\w+)/(?P<doc>\w+)/$', consumers.DocumentConsumer.as_asgi()),
]
>>>>>>> 193076cf095e1cf2b4ad889d7eb75c93e4744e43
