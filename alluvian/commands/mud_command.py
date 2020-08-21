from typing import List, Dict

from alluvian.server.mudserver import MudServer
from players.models import Player
from server.connection_session import ConnectionSession
from constants import PlayerType
'''
The basic mud command.  All regular commands shoudl extend the mudcommand such that they are classes.
'''
class MudCommand(object):
    mud_server: MudServer
    sessions: List[ConnectionSession]
    actor: Player
    arguments: Dict
    key: str
    alias: List[str]
    level: PlayerType

    key = ''
    aliases = []
    level = PlayerType.PLAYER

    def __init__(self, mud_server, sessions, actor):
        self.mud_server = mud_server
        self.sessions = sessions
        self.actor = actor

    def help(self):
        return """
        This is an example help file
        """

    def execute(self):
        self.msg('Huh?!')

    def msg(self, msg):
        return self.mud_server.send_message(self.actor, msg)
