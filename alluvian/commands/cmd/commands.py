from alluvian.commands.mud_command import MudCommand
import alluvian.globals
from commands.interpreter import Interpreter


class Commands(MudCommand):

    key = 'commands'
    aliases = ['command', 'cmd']

    def execute(self):
        commands = Interpreter.build_cmd_list(alluvian.globals.players[self.actor].player)
        msg = "The following commands are available to you: \r\n"

        for idx, command in enumerate(commands):
            msg += command['key']

            if idx % 4 == 0 and idx != 0:
                msg += '\r\n'
            else:
                msg += '\t'

        self.msg(msg)



