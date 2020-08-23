from alluvian.commands.mud_command import MudCommand

class Say(MudCommand):

    key = 'say'
    aliases = ['sa']

    def execute(self):
        self.msg("You say: {}".format(self.arguments))
        self.msg_room("{} says: {}".format(self.player.name, self.arguments))
