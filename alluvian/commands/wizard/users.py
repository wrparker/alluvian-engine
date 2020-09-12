from alluvian.commands.mud_command import MudCommand
import alluvian.globals as globs
from players.level import Level
from beautifultable import BeautifulTable

class Users(MudCommand):

    key = 'users'
    aliases = []

    level = Level.IMPL


    def execute(self):
        table = BeautifulTable()
        table.columns.header = ['Num', 'Name', 'IPAddr']
        table.set_style(BeautifulTable.STYLE_COMPACT)
        table.columns.alignment = BeautifulTable.ALIGN_LEFT
        for pid, pl in globs.sessions.items():
            try:
                table.rows.append([pid, pl.player.name, globs.mud.get_player_ip(pid)])
            except AttributeError:
                table.rows.append(['Unidentified', globs.mud.get_player_ip(pid)])
        msg = f'{table}\r\n\r\n'
        msg += f'{len(table.rows)} visible Sockets connected'
        self.msg(msg)
