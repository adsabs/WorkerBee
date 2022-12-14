import os
import sys
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from .commands.say import Say
from .commands.help import Help
from ...bridge import BridgeBot
from ...bridge import Command

class SlackBot(BridgeBot):
    def __init__(self, bot_name="slack-bot"):
        super().__init__(bot_name)

        try:
            SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
        except KeyError:
            print("'SLACK_BOT_TOKEN' needs to be defined as a environment variable")
            sys.exit(1)
        try:
            SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']
        except KeyError:
            print("'SLACK_APP_TOKEN' needs to be defined as a environment variable")
            sys.exit(1)

        self.app = App(token=SLACK_BOT_TOKEN)
        self.bot_handler = SocketModeHandler(self.app, SLACK_APP_TOKEN)
        self.app.event("app_mention")(self.mention_handler)
        self.app.event("message")(self.handle_message_events)
        self.available_commands = {
            'say': Say(self.app.client),
            'help': Help(bot_name),
        }


    def start(self):
        #self.bot_handler.start() # start() blocks, but connect() does not and we can run a worker in parallel
        self.bot_handler.connect()
        super().start()

    def react(self, msg):
        command, payload = self.decompose(msg)
        if command in self.available_commands:
            return self.available_commands[command].run(payload)
        elif len(payload) > 0:
            bot_name, command = self.decompose(msg)
            cmd = Command(bot_name)
            return cmd.run(command)
        elif len(command) > 0:
            return "Unknown command: `{}`. Type `@WorkerBee help` for help.".format(command)
        else:
            return "Unknown command. Type `@WorkerBee help` for help."

    def mention_handler(self, event, say):
        # Mention in channel
        msg = self.parse(event)
        response = self.react(msg)
        say(response)

    def handle_message_events(self, event, say):
        # Direct message
        msg = self.parse(event)
        response = self.react(msg)
        say(response)

    def parse(self, msg):
        """Parse received event and extract clean text payload"""
        payload = ''
        blocks = msg.get('blocks')
        if blocks:
            # Instead of using the whole raw text (i.e., event.get('text', '')), use the parsed text and ignore mentions, emojis, etc...
            for block in blocks:
                if block.get('type', '') in ('rich_text',):
                    for element in block.get('elements', []):
                        if element.get('type', '') in ('rich_text_section',):
                            for subelement in element.get('elements', []):
                                if subelement.get('type', '') == 'text':
                                    payload += subelement.get('text', '')
                                elif subelement.get('type', '') == 'link':
                                    payload += subelement.get('url', '')
                                elif subelement.get('type', '') == 'channel':
                                    payload += subelement.get('channel_id', '')
        return payload


