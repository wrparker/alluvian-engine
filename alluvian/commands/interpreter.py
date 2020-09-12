import pkgutil
import importlib
from typing import AbstractSet, Type

from django.conf import settings
from alluvian.commands.mud_command import MudCommand


class Interpreter:

    cmd_list = []

    def __init__(self):
        self.cmd_list = self.build_cmd_list()

    def all_subclasses(self, package, cls):
        for importer, modname, ispkg in pkgutil.iter_modules([package[0]]):
            # Classes have to be imported for subclass detection to work.
            importlib.import_module(f'{package[1]}.{modname}')
        return set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in self.all_subclasses(package, c)])

    def get_cmd_classes(self) -> AbstractSet[MudCommand]:
        retval = []
        for package in settings.CMD_PATHS:
            retval.extend(self.all_subclasses(package, MudCommand))

        return retval

    def build_cmd_list(self):
        cmd_list = []
        for cmd in self.get_cmd_classes():
            if cmd.key.strip() and cmd.key not in [k['key'] for k in cmd_list]:
                cmd_list.append({
                    'key': cmd.key.lower(),
                    'aliases': [alias.lower() for alias in cmd.aliases],
                    'module': cmd,
                    'level': cmd.level
                 })
        return cmd_list

    def cmd_search(self, inp, player) -> Type[MudCommand]:
        inp = inp.lower()
        commands = [c for c in self.cmd_list if player.level >= c['level']]

        for cmd in commands:
            if inp == cmd['key']:
                return cmd['module']
            if inp in cmd['aliases']:
                return cmd['module']
        return MudCommand

    def exec_cmd(self, pid, key, arguments=None):
        cmd = [c for c in self.cmd_list if c['key'].lower() == key.lower()][0]
        cmd['module'](pid, arguments).execute()

