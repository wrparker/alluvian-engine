import sys
import pkgutil
import importlib
from typing import List, Set, AbstractSet, Callable, Union

from django.conf import settings
from alluvian.commands.mud_command import MudCommand


class CommandInterpreter:

    @staticmethod
    def all_subclasses(cls):
        for importer, modname, ispkg in pkgutil.iter_modules(settings.CMD_PATHS):
            # Classes have to be imported for subclass detection to work.
            importlib.import_module('commands.cmd.'+ modname)
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
    def cmd_search(cmd_in) -> MudCommand:
        cmd_in = cmd_in.lower()
        commands = CommandInterpreter.build_cmd_list()

        for cmd in commands:
            if cmd_in == cmd['key']:
                return cmd['module']
            if cmd_in in cmd['aliases']:
                return cmd['module']
        return MudCommand


