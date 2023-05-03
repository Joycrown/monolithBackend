from block.consumers import TimelineConsumer
from django.urls import re_path 


websocket_urlpatterns = [
    re_path(r'^ws/timeline/(?P<user_id>\w+)', TimelineConsumer.as_asgi()),
]