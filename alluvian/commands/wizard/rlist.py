from beautifultable import BeautifulTable
from alluvian.commands.mud_command import MudCommand
from util.colors import Colors
from world.models import Room, Zone
from players.level import Level

class Rlist(MudCommand):

    key = 'rlist'
    aliases = ['rl', 'rli', 'rlis']

    level = Level.IMM

    def execute(self):
        if not self.arguments:
            z = Zone.objects.get(pk=self.room.zone_id)
        else:
            z = Zone.objects.get(pk=self.arguments.split()[0])

        rlist = Room.objects.filter(zone=z)

        if not rlist:
            self.msg(f"No rooms found in zone {z.id}")
        else:
            table = BeautifulTable(default_padding=0)
            table.column_headers = ['Index', 'Room Name']
            table.set_style(BeautifulTable.STYLE_COMPACT)
            table.columns.alignment = BeautifulTable.ALIGN_LEFT
            table.column_alignments['Index'] = BeautifulTable.ALIGN_RIGHT
            table.column_widths = [7, 44]
            table.columns.header.alignment = BeautifulTable.ALIGN_LEFT
            for r in rlist:
                table.rows.append([f'{r.id})', f'{Colors.fg.CYAN}{r.name}{Colors.style.RESET_ALL}'])
            self.msg(table)
