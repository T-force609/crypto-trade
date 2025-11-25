from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()

@database_sync_to_async
def get_user(token):
    try:
        access_token = AccessToken(token)
        return User.objects.get(id=access_token["user_id"])
    except Exception:
        return None

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        token = query_params.get("token")
        if token:
            user = await get_user(token[0])
            scope["user"] = user
        return await super().__call__(scope, receive, send)
