from alluvian.commands.mud_command import MudCommand
import alluvian.globals as globs
from players.level import Level
from tabulate import tabulate

class Users(MudCommand):

    key = 'users'
    aliases = []

    level = Level.IMPL


    def execute(self):
        data = []
        headers = ['User', 'IPAddr']
        for pid, pl in globs.sessions.items():
            try:
                data.append([pl.player.name, globs.mud.get_player_ip(pid)])
            except AttributeError:
                data.append(['Unidentified', globs.mud.get_player_ip(pid)])
        table = tabulate(data, headers)
        msg = f'{table}\r\nTotal Connected Users: {len(globs.sessions.items())}'
        self.msg(msg)
