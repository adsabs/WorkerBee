import os
import sys
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from .commands import Command

try:
    SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
except:
    print("'SLACK_BOT_TOKEN' needs to be defined as a environment variable")
    sys.exit(1)
try:
    SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']
except:
    print("'SLACK_APP_TOKEN' needs to be defined as a environment variable")
    sys.exit(1)

app = App(token=SLACK_BOT_TOKEN)

@app.event("app_mention")
def mention_handler(body, say):
    command = Command(body)
    response = command.run()
    say(response)

@app.event("message")
def handle_message_events(body, say):
    command = Command(body)
    response = command.run()
    say(response)

bot_handler = SocketModeHandler(app, SLACK_APP_TOKEN)
