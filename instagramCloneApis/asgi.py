"""
ASGI config for instagramCloneApis project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

"""
ASGI config for instagramCloneApis project.
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "instagramCloneApis.settings")

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter

django_asgi_app = get_asgi_application()

# Now it's safe to import URLs (after Django has initialized)
from chats.urls import websocket_urlpatterns as chat_ws_urls

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(chat_ws_urls)
    ),
})
