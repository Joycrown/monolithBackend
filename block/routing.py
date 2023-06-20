from block.consumers import TimelineConsumer
from django.urls import re_path 
from chat import consumers

from django.conf.urls import url  

websocket_urlpatterns = [
    re_path(r'^ws/timeline/(?P<user_id>\w+)', TimelineConsumer.as_asgi()),
    url(r'ws/chatroom/(?P<chatroom_id>\w+)', consumers.ChatConsumer.as_asgi())
]