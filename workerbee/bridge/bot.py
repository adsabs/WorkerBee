import os
import sys
import websockets
import asyncio
from .base import BridgeBase

class BridgeBot(BridgeBase):
    def __init__(self, bot_name):
        super().__init__()
        self.bot_name = bot_name
        self.available_commands = {}

    def start(self):
        asyncio.run(self.dialog())

    async def dialog(self):
        uri = f"ws://{self.bridge_username}:{self.bridge_password}@{self.bridge_hostname}:{self.bridge_port}"
        async for websocket in websockets.connect(uri): # loop to allow re-connections (retries with exponential backoff, it first delays re-connect at three seconds and increases up to one minute)
            await websocket.send(f"register {self.bot_name}")
            response = await websocket.recv()
            if response.startswith("ERROR"):
                raise Exception(response)
            try:
                async for msg in websocket:
                    command, payload = self.decompose(msg)
                    proxy_request = command == "proxy"
                    if proxy_request:
                        requesting_bot, command = self.decompose(payload)
                        #print("[PROXY]")
                    else:
                        command = msg

                    #print(">>> " + command)
                    response = self.react(command)

                    if proxy_request:
                        await websocket.send(f"proxy {requesting_bot} {response}")
                        #print("<<< " + f"proxy {requesting_bot} {response}")
                        proxied = await websocket.recv()
                    else:
                        await websocket.send(response)
                        #print("<<< " + response)
            except websockets.ConnectionClosed:
                continue

    def react(self, msg):
        raise NotImplementedError

