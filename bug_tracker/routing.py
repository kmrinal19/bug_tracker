from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import tracker.routing
from tracker.knoxAuthSockets import TokenAuthMiddleware

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            tracker.routing.websocket_urlpatterns
        )
    ),
})
