from alluvian.commands.mud_command import MudCommand
import alluvian.globals
from commands.command_interpreter import CommandInterpreter


class Commands(MudCommand):

    key = 'commands'
    aliases = ['command', 'cmd']

    def execute(self):
        commands = CommandInterpreter.build_cmd_list()
        msg = "The following commands are available to you: \r\n"

        for idx, command in enumerate(commands):
            msg += command['key']

            if idx % 4 == 0 and idx != 0:
                msg += '\r\n'
            else:
                msg += '\t'

        self.msg(msg)



