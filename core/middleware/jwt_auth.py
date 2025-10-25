from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()
        params = parse_qs(query_string)
        token = params.get("token")

        if token:
            try:
                # import here so it only runs after Django is ready
                from rest_framework_simplejwt.tokens import AccessToken
                access_token = AccessToken(token[0])

                user = await self.get_user(access_token["user_id"])
                scope["user"] = user
            except Exception:
                scope["user"] = None
        else:
            scope["user"] = None

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
