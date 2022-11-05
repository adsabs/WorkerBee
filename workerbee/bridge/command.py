import os
import sys
import websockets
import asyncio
import nest_asyncio
nest_asyncio.apply() # necessary to allow running Command from slack-bot when reacting to a slack event
from .base import BridgeBase

class Command(BridgeBase):
    def __init__(self, bot_name):
        super().__init__()
        self.bot_name = bot_name # target bot name

    def run(self, command):
        if self.bot_name == "bridge":
            code, result = asyncio.run(self.bridge(command))
        else:
            code, result = asyncio.run(self.proxy(command))
        return result

    async def proxy(self, command):
        """Run a bot command proxying through the bridge"""
        uri = f"ws://{self.bridge_username}:{self.bridge_password}@{self.bridge_hostname}:{self.bridge_port}"
        async with websockets.connect(uri) as websocket:
            await websocket.send(f"proxy {self.bot_name} {command}")
            proxied = await websocket.recv()
            if proxied.startswith("SUCCESS"): # proxied succesfully, read response
                response = await websocket.recv()
                try:
                    proxy, payload = self.decompose(response)
                    from_bot_name, result = self.decompose(payload)
                    code = "SUCCESS"
                except ValueError:
                    return ("ERROR", "Response did not contain a code and a result")
                return (code, result)
            else:
                code, result = self.decompose(proxied)
                return ("ERROR", result)

    async def bridge(self, command):
        """Run a bridge command"""
        uri = f"ws://{self.bridge_username}:{self.bridge_password}@{self.bridge_hostname}:{self.bridge_port}"
        async with websockets.connect(uri) as websocket:
            await websocket.send(command)
            response = await websocket.recv()
            try:
                code, result = self.decompose(response)
            except ValueError:
                return ("ERROR", "Response did not contain a code and a result")
            return (code, result)

