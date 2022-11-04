import os
import sys
import websockets
import asyncio
from .base import BridgeBase

class Command(BridgeBase):
    def __init__(self, bot_name):
        super().__init__()
        self.bot_name = bot_name # target bot name
        self.bridge_username = "cli"

    def run(self, command):
        print(f">>> {self.bot_name} {command}")
        loop = asyncio.get_event_loop()
        (code, result), = loop.run_until_complete(asyncio.gather(self.bot_command(command)))
        print(f"<<< {result}")

    async def bot_command(self, command):
        uri = f"ws://{self.bridge_username}:{self.bridge_password}@{self.bridge_hostname}:{self.bridge_port}"
        async with websockets.connect(uri) as websocket:
            await websocket.send(f"{self.bot_name} {command}")
            response = await websocket.recv()
            try:
                code, result = response.split(maxsplit=1)
            except ValueError:
                return ("ERROR", "Response did not contain a code and a result")
            return (code, result)


