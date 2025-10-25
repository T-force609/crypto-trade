from channels.generic.websocket import AsyncJsonWebsocketConsumer

class PriceConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if user and user.is_authenticated:
            await self.accept()
            print(f"✅ WebSocket connected for {user.username}")
        else:
            print("❌ Invalid or missing JWT — closing connection.")
            await self.close(code=4001)

    async def receive_json(self, content, **kwargs):
        print("Received:", content)

    async def disconnect(self, code):
        print(f"🔌 Disconnected with code {code}")
