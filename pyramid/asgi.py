import os
import sys
import django
from channels.routing import get_default_application
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyramid.settings')
# django.setup()
application = get_asgi_application()


#import os
#import django
# from decouple import config

#from channels.auth import AuthMiddlewareStack

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyramid.settings')

#django.setup()

#from channels.routing import ProtocolTypeRouter, URLRouter

#from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
#import chat.routing as ChatRouting


 
#routes = ChatRouting.websocket_urlpatterns 



#application = ProtocolTypeRouter({
#    "websocket": 
    # AuthMiddlewareStack(
#        URLRouter(
#            routes
#        )
#    # ),
#})