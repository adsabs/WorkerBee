import os
import sys
import signal
import asyncio
import websockets
from .base import BridgeBase

class Bridge(BridgeBase):
    def __init__(self):
        super().__init__()
        self.registered_bots = {}
        self.reserved_bot_names = ("-",)
        self.credentials = (("bot", self.bridge_password), ("cli", self.bridge_password))

    def start(self):
        asyncio.run(self.bridge())

    async def bridge(self):
        async with websockets.serve(
            self.bridge_handler, self.bridge_hostname, self.bridge_port,
            create_protocol=websockets.basic_auth_protocol_factory(
                realm="WorkerBee", credentials=self.credentials
            ),
        ):
            await asyncio.Future()  # run forever

    async def bridge_handler(self, websocket):
        if websocket.username.startswith("bot"):
            bot_name = await websocket.recv() # First message is the name of the just connected process
            if len(bot_name) == 0 or bot_name in self.reserved_bot_names:
                await websocket.close()
            else:
                print(f"Connected: bot '{bot_name}'")
                self.registered_bots[bot_name] = websocket
                try:
                    # I am a bot, wait for commands
                    await websocket.wait_closed()
                finally:
                    del self.registered_bots[bot_name]
        else:
            print("Connected: non-bot")
            # I am a not a bot, I just want to send a command to a bot
            async for bot_command in websocket:
                try:
                    bot_name, command = bot_command.split(maxsplit=1)
                except ValueError:
                    await websocket.send(f"ERROR Unable to find bot name and command in '{bot_command}'")
                else:
                    bot = self.registered_bots.get(bot_name)
                    if bot is not None:
                        try:
                            await bot.send(command)
                            response = await bot.recv()
                        except websockets.ConnectionClosed:
                            del self.registered_bots[bot_name]
                            await websocket.send(f"ERROR Connection lost, no bot with name '{bot_name}'")
                        finally:
                            await websocket.send(f"SUCCESS {response}")
                    else:
                        bot_names = ", ".join([n for n in self.registered_bots.keys()])
                        if bot_name in self.reserved_bot_names and command == "list":
                            await websocket.send(f"SUCCESS '{bot_names}'")
                        else:
                            await websocket.send(f"ERROR No bot with name '{bot_name}', registered bots: '{bot_names}'")


