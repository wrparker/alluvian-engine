from alluvian.commands.mud_command import MudCommand
import alluvian.globals as globs
from players.level import Level
from util.colors import Colors

from commands.cmd.look import Look


class Goto(MudCommand):

    key = 'goto'
    aliases = []

    level = Level.IMM

    def execute(self):
        if not self.arguments:
            self.msg("Goto where?")
        else:
            try:
                room_id = int(self.arguments.split()[0])
                if globs.rooms[room_id]:
                    self.msg_room(f'{Colors.fg.BRED}{globs.sessions[self.actor].player.name} disappears in a puff of smoke.{Colors.style.RESET_ALL}')
                    globs.sessions[self.actor].player.room = room_id
                    self.room = globs.sessions[self.actor].player.room
                    self.msg_room(f'{Colors.fg.BRED}{globs.sessions[self.actor].player.name} appears with an ear-splitting bang.{Colors.style.RESET_ALL}')
                    self.call_command(Look)
            except (IndexError, KeyError):
                self.msg("That room number does not exist.")
            except ValueError:
                self.msg("Goto can only be a room number at this time (integer).")


