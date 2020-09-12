from alluvian.commands.mud_command import MudCommand
from util.colors import Colors
from world.models import Zone
from players.level import Level
from beautifultable import BeautifulTable

class Rlist(MudCommand):

    key = 'zlist'
    aliases = ['zl', 'zli', 'zlis']

    level = Level.IMM

    def execute(self):
        zlist = Zone.objects.all()
        table = BeautifulTable(default_padding=0)
        table.column_headers = ['Index', 'Zone Name']
        table.set_style(BeautifulTable.STYLE_COMPACT)
        table.columns.alignment = BeautifulTable.ALIGN_LEFT
        table.column_alignments['Index'] = BeautifulTable.ALIGN_RIGHT
        table.column_widths = [7, 44]
        table.columns.header.alignment = BeautifulTable.ALIGN_LEFT

        if not zlist:
            self.msg(f"No Zones to show!")
        else:
            for z in zlist:
                table.rows.append([f'{z.id})', f'{Colors.fg.CYAN}{z.name}{Colors.style.RESET_ALL}'])

        self.msg(table)
