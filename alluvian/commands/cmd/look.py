from alluvian.commands.mud_command import MudCommand

import alluvian.globals as glob

from util.colors import Colors

class Look(MudCommand):
    key = 'look'
    aliases = ['l', 'loo']

    def execute(self):
        user = glob.sessions[self.actor]

        msg = f'{Colors.fg.BCYAN}{user.player.room.name}{Colors.style.RESET_ALL}\r\n' \
              f'{Colors.fg.CYAN}{user.player.room.description}{Colors.style.RESET_ALL}\r\n'

        # Get all players that are not the current player.
        for connection_id, player in self.get_players_in_room().items():
            if connection_id != self.actor:
                msg += f'{Colors.fg.BGREEN}{player.name} is standing here.{Colors.style.RESET_ALL}\r\n'

        # Get Exits
        msg += Colors.fg.BBLUE
        msg += 'Obvious Exits\r\n'
        # TODO: case for no exits
        if self.room.exit_north:
            msg += f'north\t - {glob.rooms[self.room.exit_north].name}'
        if self.room.exit_east:
            msg += f'east\t - {glob.rooms[self.room.exit_east].name}'
        if self.room.exit_west:
            msg += f'west\t - {glob.rooms[self.room.exit_west].name}'
        if self.room.exit_south:
            msg += f'south\t - {glob.rooms[self.room.exit_south].name}'
        # TODO: Add up
        # TODO: Add down
        msg += Colors.style.RESET_ALL

        self.msg(msg)


