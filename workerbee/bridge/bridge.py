import os
import sys
import signal
import asyncio
import websockets
from .base import BridgeBase

class Bridge(BridgeBase):
    def __init__(self):
        super().__init__()
        self.stdout = True
        self.registered_bots = {}
        self.registered_bot_names = {}
        self.bridge_name = 'bridge'
        self.credentials = ((self.bridge_username, self.bridge_password), )
        self.available_commands = {
            'register': self.register,
            'deregister': self.deregister,
            'proxy': self.proxy,
            'list': self.list,
            'help': self.help,
        }

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
        await self.register(websocket, 'unnamed')
        try:
            async for payload in websocket:
                command, payload = self.decompose(payload)

                if self.stdout:
                    if command == "proxy":
                        print(command, payload.split("\n")[0])
                    else:
                        print(command, payload)

                if command in self.available_commands:
                    code, response = await self.available_commands[command](websocket, payload)
                elif len(command) > 0:
                    code, response = "ERROR", f"Unknown command: `{command}`"
                else:
                    code, response = "ERROR", f"Unknown command"
                await websocket.send(f"{code} {response}")
        except websockets.ConnectionClosed:
            pass
        finally:
            await self.deregister(websocket, [])


    #--------------------------------------------------------------------------------
    async def register(self, websocket, payload):
        bot_name, _ = self.decompose(payload)
        if len(bot_name) > 0:
            if bot_name == self.bridge_name:
                code = "ERROR"
                response = f"'{bot_name}' is a reserved name"
            else:
                self.registered_bots[str(websocket.id)] = (bot_name, websocket)
                if bot_name != "unnamed":
                    self.registered_bot_names[bot_name] = str(websocket.id)
                code = "SUCCESS"
                response = "registered"
        else:
            code = "ERROR"
            response = "Missing argument"
        return code, response

    async def deregister(self, websocket, payload):
        bot_id = str(websocket.id)
        bot_name, _ = self.registered_bots.pop(bot_id, ('', None))
        if bot_name in self.registered_bot_names:
            del self.registered_bot_names[bot_name]
        if bot_name:
            code = "SUCCESS"
            response = "Deregistered"
        else:
            code = "ERROR"
            response = "Missing argument"
        return code, response

    async def list(self, websocket, payload):
        code = "SUCCESS"
        response = f"{', '.join([self.bridge_name] + [n for n in self.registered_bot_names.keys()])}"
        return code, response

    async def proxy(self, websocket, payload):
        from_bot_name, _ = self.registered_bots.get(str(websocket.id), "unnamed")
        if from_bot_name == "unnamed":
            from_bot_name = str(websocket.id)
        to_bot_name, command = self.decompose(payload)
        if len(to_bot_name) > 0 and len(command) > 0:
            _, bot = self.registered_bots.get(self.registered_bot_names.get(to_bot_name), self.registered_bots.get(to_bot_name, ('', None))) # to_bot_name may be a name or directly an ID, try both
            if bot is not None:
                try:
                    await bot.send(f"proxy {from_bot_name} {command}")
                    #response = await bot.recv()
                    code = "SUCCESS"
                    response = "Proxied"
                except websockets.ConnectionClosed:
                    await self.deregister(bot, [])
                    code = "ERROR"
                    response = f"Connection lost [{to_bot_name}]"
                else:
                    code = "SUCCESS"
                    response = f"{response}"
            else:
                bot_names = ", ".join([self.bridge_name] + [n for n in self.registered_bot_names.keys()])
                code = "ERROR"
                response = f"No bot with name '{to_bot_name}', registered bots: '{bot_names}'"
        else:
            code = "ERROR"
            response = "Missing arguments"
        return code, response

    async def help(self, websocket, payload):
        code = "SUCCESS"
        output = f"> Use `{self.bridge_name}` followed by one of these commands:\n"
        output += """\t- `list`: list registered bots\n"""
        #output += """\t- `help`: print instructions\n"""
        return code, output
