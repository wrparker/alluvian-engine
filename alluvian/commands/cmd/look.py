from alluvian.commands.mud_command import MudCommand

import alluvian.globals as glob

from util.colors import Colors
from util.asciimap import show_map

class Look(MudCommand):
    key = 'look'
    aliases = ['l', 'loo']

    def execute(self):
        user = glob.sessions[self.actor]

        msg = f'{Colors.fg.BCYAN}{user.player.room.name}{Colors.style.RESET_ALL}\r\n' \
              f'{Colors.fg.CYAN}{user.player.room.description}{Colors.style.RESET_ALL}\r\n'

        msg += show_map(self.room) + '\r\n'
        # Get all players that are not the current player.
        for connection_id, player in self.get_players_in_room().items():
            if connection_id != self.actor:
                msg += f'{Colors.fg.BGREEN}{player.name} is standing here.{Colors.style.RESET_ALL}\r\n'

        # Get Exits
        msg += Colors.fg.BBLUE
        msg += 'Obvious Exits\r\n'
        if not self.room.has_exits():
            msg += f'{Colors.fg.BWHITE}None.'
        else:
            exits = [att for att in dir(self.room) if att.startswith('exit_')]
            for exit in exits:
                if getattr(self.room, exit):
                    direction = exit.replace("exit_", "")
                    msg += f'{direction}\t - {glob.rooms[getattr(self.room, exit)].name}\r\n'
        msg += Colors.style.RESET_ALL
        self.msg(msg)


