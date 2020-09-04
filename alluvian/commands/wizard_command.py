from mud_command import MudCommand
from alluvian.players.level import Level

class WizardCommand(MudCommand):
    level = Level.IMM

    def __init__(self, mud_server, actor, arguments):
        super().__init__(self, mud_server, actor, arguments)
