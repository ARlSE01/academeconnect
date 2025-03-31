import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "academeconnect.settings")
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from . import routing

application = ProtocolTypeRouter(
    {
        "https": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )
        ),
    }
)
