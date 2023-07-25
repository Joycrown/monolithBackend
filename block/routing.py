from block.consumers import TimelineConsumer
from django.urls import re_path 
from message.consumers import ChatConsumer

from django.conf.urls import url  

websocket_urlpatterns = [
    re_path(r'^ws/timeline/(?P<user_id>\w+)', TimelineConsumer.as_asgi()),
    url(r'ws/chat/(?P<username>\w+)', ChatConsumer.as_asgi())
]