from alluvian.commands.mud_command import MudCommand

class Look(MudCommand):
    key = 'look'
    aliases = ['l', 'loo']

    def execute(self):
        self.mud_server.send_message(self.actor, 'Ok you did it!')
