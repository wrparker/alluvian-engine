from alluvian.commands.mud_command import MudCommand
import alluvian.globals

class Gecho(MudCommand):

    key = 'gecho'
    aliases = []

    def execute(self):
        for pid, pl in alluvian.globals.players.items():
            self.mud_server.send_message(pid, 'OK')