from .say import Say
from ....bridge import Command

class Help(object):
    def __init__(self, bot_name):
        self.bot_name = bot_name

    def run(self, arguments):
        output = ""
        #output = f"> Use `{self.bot_name}` followed by one of these commands:\n"
        #output += self.help()
        #output += Say(None).help()
        #
        bot_name, command = "bridge", "list"
        cmd = Command(bot_name)
        registered_bots = cmd.run(command).split(", ")
        for registered_bot in registered_bots:
            if registered_bot in (self.bot_name,):
                continue
            cmd = Command(registered_bot)
            output += cmd.run("help")
        return output

    def help(self):
        return """\t- `help`: print instructions\n"""

