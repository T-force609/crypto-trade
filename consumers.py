from channels.generic.websocket import AsyncJsonWebsocketConsumer

class PriceConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        if not self.scope.get("user") or not self.scope["user"].is_authenticated:
            await self.close()
            return
        await self.accept()
