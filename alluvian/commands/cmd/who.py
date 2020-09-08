from alluvian.commands.mud_command import MudCommand
import alluvian.globals
from menus.new_connection import LoginState
from django.conf import settings

class Who(MudCommand):

    key = 'who'
    aliases = []

    def execute(self):
        logged_in = [pl for pid, pl in alluvian.globals.sessions.items() if pl.login_state == LoginState.AUTHENTICATED]
        msg = 'Level\tName\r\n'
        border = ''
        while len(border) < settings.MAX_LINE_WIDTH:
            border += '='
        msg += f'{border}\r\n'
        for pl in logged_in:
            msg += f'{pl.player.level}\t{pl.player.name}\r\n'
        msg += f'Total Connected Players: {len(logged_in)}'

        self.msg(msg)
