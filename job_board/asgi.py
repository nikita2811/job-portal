"""
ASGI config for job_board project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import job_board.routing
from jobs.middleware import JWTAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_board.settings')


application = ProtocolTypeRouter({
    'http':      get_asgi_application(),            # normal HTTP requests
    'websocket': JWTAuthMiddleware(               # websocket requests
        URLRouter(
            job_board.routing.websocket_urlpatterns
        )
    )
})
