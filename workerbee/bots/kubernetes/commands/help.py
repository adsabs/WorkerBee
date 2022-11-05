from .show import Show

class Help(object):
    def __init__(self, bot_name):
        self.bot_name = bot_name

    def run(self, arguments):
        output = f"> Use `{self.bot_name}` followed by one of these commands:\n"
        #output += self.help()
        output += Show().help()
        return output

    def help(self):
        return """\t- `help`: print instructions\n"""

