import os
import sys
import websockets
import asyncio
from .base import BridgeBase

class BridgeBot(BridgeBase):
    def __init__(self, bot_name):
        super().__init__()
        self.bot_name = bot_name

    def start(self):
        asyncio.run(self.dialog())

    async def dialog(self):
        uri = f"ws://{self.bridge_username}:{self.bridge_password}@{self.bridge_hostname}:{self.bridge_port}"
        async for websocket in websockets.connect(uri): # loop to allow re-connections (retries with exponential backoff, it first delays re-connect at three seconds and increases up to one minute)
            await websocket.send(self.bot_name)
            try:
                async for msg in websocket:
                    response = self.react(msg)
                    await websocket.send(response)
            except websockets.ConnectionClosed:
                continue

    def react(self, msg):
        raise NotImplementedError

