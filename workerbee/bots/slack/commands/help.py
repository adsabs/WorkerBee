from .say import Say
from .show import Show

class Help(object):

    def run(self, arguments):
        output = "You can interact with me using the following commands:\n"
        output += self.help()
        output += Show().help()
        #output += Say(None).help() # Hide from users, only useful internally
        return output

    def help(self):
        return """- `help`: print instructions\n"""

