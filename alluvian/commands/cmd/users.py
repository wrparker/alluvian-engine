from alluvian.commands.mud_command import MudCommand
import alluvian.globals as globs
from players.level import Level

class Users(MudCommand):

    key = 'users'
    aliases = []

    level = Level.IMPL

    def execute(self):
        for pid, pl in globs.players.items():
            try:
                self.msg(f'{pl.player.name}: {globs.mud.get_player_ip(pid)}\r\n')
            except AttributeError:
                self.msg(f'Unidentified: {globs.mud.get_player_ip(pid)}\r\n')
        self.msg(f'{len(globs.players.items())} connected Users')
