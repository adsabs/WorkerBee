from .show import Show
from .help import Help

class Command(object):
    def __init__(self, payload):
        self.available_commands = {
            'show': Show(),
            'help': Help(),
        }
        self.command = ''
        self.arguments = []
        self._parse(payload)


    def _parse(self, payload):
        """Parse received event and extract command and arguments"""
        event = payload.get('event')
        if event:
            event_type = event.get('type', {})
            if event_type in ('app_mention', 'message'):
                # Instead of using the whole raw text (i.e., event.get('text', '')), use the parsed text and ignore mentions, emojis, etc...
                raw_text = ''
                for block in event.get('blocks', []):
                    for element in block.get('elements', []):
                        if element.get('type', '') in ('rich_text_section', 'link'):
                            for subelement in element.get('elements', []):
                                if subelement.get('type', '') == 'text':
                                    raw_text += subelement.get('text', '')
                splitted_raw_text = raw_text.split() # Example: '<@U047JJZL4LQ> show ads-dev ads-prod'
                if len(splitted_raw_text) > 0:
                    self.command = splitted_raw_text[0] # Example: 'show'
                    self.arguments = splitted_raw_text[1:] # Example: ['ads-dev', 'ads-prod']

    def run(self):
        if self.command in self.available_commands:
            return self.available_commands[self.command].run(self.arguments)
        elif len(self.command) > 0:
            return "Unknown command: `{}`. Type `@WorkerBee help` for help.".format(self.command)
        else:
            return "Unknown command. Type `@WorkerBee help` for help."


