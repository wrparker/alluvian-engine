from alluvian.commands.mud_command import MudCommand
import alluvian.globals
import alluvian.globals as glob


class Commands(MudCommand):

    key = 'commands'
    aliases = ['command', 'cmd']

    def execute(self):
        commands = [c for c in glob.interpreter.cmd_list if glob.sessions[self.actor].player.level >= c['level']]
        msg = "The following commands are available to you: \r\n"

        for idx, command in enumerate(commands):
            msg += command['key']

            if idx % 4 == 0 and idx != 0:
                msg += '\r\n'
            else:
                msg += '\t'

        self.msg(msg)



