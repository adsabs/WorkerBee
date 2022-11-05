from .commands.show import Show
from .commands.help import Help

from ...bridge import BridgeBot

class KubernetesBot(BridgeBot):
    def __init__(self, bot_name="kubernetes-bot"):
        super().__init__(bot_name)
        self.available_commands = {
            'show': Show(),
            'help': Help(bot_name),
        }

    def react(self, msg):
        command, arguments = self.decompose(msg)
        if command in self.available_commands:
            return self.available_commands[command].run(arguments)
        elif len(command) > 0:
            return "Unknown command: `{}`".format(msg)
        else:
            return "Unknown command"


