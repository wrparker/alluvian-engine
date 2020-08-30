from typing import List, Dict

from alluvian.server.mudserver import MudServer
from players.models import Player
from players.level import Level
from server.connection_session import ConnectionSession
from world.models import Room

import alluvian.globals
'''
The basic mud command.  All regular commands should extend the mudcommand such that they are classes.
'''
class MudCommand(object):
    mud_server: MudServer
    sessions: List[ConnectionSession]
    actor: Player
    arguments: List[str]
    key: str
    alias: List[str]
    level: int
    room: Room

    key = ''
    aliases = []
    level = 1

    def __init__(self, mud_server, actor, arguments):
        self.mud_server = mud_server
        self.actor = actor
        self.arguments = arguments
        self.session = alluvian.globals.players[actor]
        self.room = alluvian.globals.rooms[self.session.room]
        self.player = self.session.player


    def help(self):
        return """
        This is an example help file
        """

    def execute(self) -> None:
        self.msg('Huh?!')

    def msg(self, msg) -> None:
        self.mud_server.send_message(self.actor, msg)

    def msg_room(self, msg) -> None:
        for connection_id, player in self.room.get_players().items():
            if connection_id != self.actor:
                self.mud_server.send_message(connection_id, msg)
