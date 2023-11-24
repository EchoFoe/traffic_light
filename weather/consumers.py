import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer


class TgConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, **kwargs):
        await asyncio.sleep(1)
        await self.send(text_data=f'Процессы в действии: {kwargs}')
