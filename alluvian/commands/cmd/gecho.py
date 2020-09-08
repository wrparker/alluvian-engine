from alluvian.commands.mud_command import MudCommand
import alluvian.globals
from players.level import Level

class Gecho(MudCommand):

    key = 'gecho'
    aliases = ['gech']

    level = Level.IMM

    def execute(self):
        for pid, pl in alluvian.globals.sessions.items():
            self.mud_server.send_message(pid, self.arguments)
