import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from auction.routing import websocket_urlpatterns
import django
# This is needed to configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_auction.settings')
django.setup()  
# Importing Django settings must happen after setting DJANGO_SETTINGS_MODULE
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
