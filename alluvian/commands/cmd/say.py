from alluvian.commands.mud_command import MudCommand

from alluvian.util.colors import Colors

class Say(MudCommand):

    key = 'say'
    aliases = ['sa']

    def execute(self):
        self.msg("{}You say, '{}'.{}".format(Colors.fg.BCYAN,
                                          self.arguments,
                                          Colors.fg.RESET))
        self.msg_room("{}{} says, '{}'.{}".format(Colors.fg.BCYAN,
                                               self.player.name,
                                               self.arguments,
                                               Colors.fg.RESET))
