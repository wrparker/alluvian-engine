from typing import Dict

from django.db import models

from players.models import Player
import alluvian.globals

class Room(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    exit_north = models.IntegerField(null=True, blank=True)
    exit_south = models.IntegerField(null=True, blank=True)
    exit_east = models.IntegerField(null=True, blank=True)
    exit_west = models.IntegerField(null=True, blank=True)

    def get_players(self) -> Dict[str, Player]:
        return {k: v for k, v in alluvian.globals.players.items() if v.room == self.id}

