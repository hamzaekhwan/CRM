



from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from django.urls import path
from CRMapp.clients import consumers
from django.core.asgi import get_asgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CRMsystem.settings')
ws_patterns=[path('ws/test/',consumers.NotificationConsumer.as_asgi())]
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket':
       
            URLRouter(ws_patterns)}
    )
    


