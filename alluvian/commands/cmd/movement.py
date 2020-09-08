from alluvian.commands.mud_command import MudCommand

from alluvian.globals import sessions

from commands.cmd.look import Look


class Movement(MudCommand):
    key = ''
    aliases = []

    def execute(self):
        user = sessions[self.actor]
        room = user.player.room

        if getattr(room, f'exit_{self.key}'):
            self.msg_room(f'{user.player.name} leaves north.\r\n')
            user.player.room = getattr(room, f'exit_{self.key}')
            self.room = user.player.room
            self.msg_room(f'{user.player.name} has arrived.\r\n')
            self.call_command(Look)

        else:
            self.msg("Alas, you cannot go that way...\r\n")

class North(Movement):
    key = 'north'
    aliases = ['nort', 'n']

class South(Movement):
    key = 'south'
    aliases = ['sout', 's']

class East(Movement):
    key = 'east'
    aliases = ['e', 'ea', 'eas']

class West(Movement):
    key = 'west'
    aliases = ['w', 'we', 'wes']
