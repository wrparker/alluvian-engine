from alluvian.commands.mud_command import MudCommand

from alluvian.globals import rooms, players


class Look(MudCommand):
    key = 'look'
    aliases = ['l', 'loo']

    def execute(self):
        user = players[self.actor]
        room = rooms[user.room]

        self.msg(room.description)
