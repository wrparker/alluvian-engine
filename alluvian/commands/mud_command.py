from typing import List, Dict

from players.models import Player
from world.models import Room

import alluvian.globals
'''
The basic mud command.  All regular commands should extend the mudcommand such that they are classes.
'''
class MudCommand(object):
    sessions: List['ConnectionSession']
    actor: Player
    arguments: List[str]
    key: str
    alias: List[str]
    level: int
    room: Room

    key = ''
    aliases = []
    level = 1

    def __init__(self, actor, arguments=None):
        self.actor = actor
        self.arguments = arguments
        self.session = alluvian.globals.sessions[actor]
        self.room = self.session.player.room
        self.player = self.session.player

    def call_command(self, cmd_class, arguments=None):
        cmd_class(self.actor, arguments).execute()

    def help(self):
        return """
        This is an example help file
        """

    def execute(self) -> None:
        self.msg('Huh?!')

    def msg(self, msg) -> None:
        alluvian.globals.mud.send_message(self.actor, msg)

    def msg_room(self, msg) -> None:
        for connection_id, player in self.get_players_in_room().items():
            if connection_id != self.actor:
                alluvian.globals.mud.send_message(connection_id, msg)

    def get_players_in_room(self) -> Dict[str, Player]:
        # TODO: probably should have utility function that gets logged in players only.
        return {k: v for k, v in alluvian.globals.sessions.items() if hasattr(v.player, 'room') and v.player.room.id == self.room.id}
