from django.db import models

from players.models import Player

class Room(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    exit_north = models.IntegerField(null=True, blank=True)
    exit_south = models.IntegerField(null=True, blank=True)
    exit_east = models.IntegerField(null=True, blank=True)
    exit_west = models.IntegerField(null=True, blank=True)
    exit_up = models.IntegerField(null=True, blank=True)
    exit_down = models.IntegerField(null=True, blank=True)

    def has_exits(self):
        exits = [att for att in dir(self) if att.startswith('exit_')]
        for exit in exits:
            if exit:
                return True
        return False
