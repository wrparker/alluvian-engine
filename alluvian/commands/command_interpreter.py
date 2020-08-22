import sys
import pkgutil
import importlib
from typing import List, Set, AbstractSet, Callable, Union

from django.conf import settings
from alluvian.commands.mud_command import MudCommand

# TODO: proabbly shouldn't be a static method, would make more sense to remturn obj with set command

class CommandInterpreter:

    @staticmethod
    def all_subclasses(cls):
        for importer, modname, ispkg in pkgutil.iter_modules(settings.CMD_PATHS):
            # Classes have to be imported for subclass detection to work.
            importlib.import_module('commands.cmd.' + modname)
        return set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in CommandInterpreter.all_subclasses(c)])

    @staticmethod
    def get_cmd_classes() -> AbstractSet[MudCommand]:
        return CommandInterpreter.all_subclasses(MudCommand)

    @staticmethod
    def build_cmd_list():
        cmd_list = []
        for cmd in CommandInterpreter.get_cmd_classes():
            cmd_list.append({
                'key': cmd.key.lower(),
                'aliases': [alias.lower() for alias in cmd.aliases],
                'module': cmd
            })
        return cmd_list

    @staticmethod
    def cmd_search(parsed_cmd) -> MudCommand:
        parsed_cmd = CommandInterpreter.parse_command(parsed_cmd.lower())
        commands = CommandInterpreter.build_cmd_list()

        for cmd in commands:
            if parsed_cmd['cmd'] == cmd['key']:
                return cmd['module'], parsed_cmd
            if parsed_cmd['cmd'] in cmd['aliases']:
                return cmd['module'], parsed_cmd
        return MudCommand, parsed_cmd

    @staticmethod
    def parse_command(command):
        command = command.strip()
        pieces = command.split(' ', 1)
        cmd = pieces[0].lower()
        try:
            args = pieces[1]
        except IndexError:
            args = None

        return {
            'cmd': cmd,
            'args': args
        }
