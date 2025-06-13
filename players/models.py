from django.db import models
from registration.models import TournamentRegistration
# Create your models here.

class LeagueAssignment(models.Model):
    team = models.OneToOneField(TournamentRegistration, on_delete=models.CASCADE)
    league = models.CharField(max_length=1)  # A, B, C...
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.team.player_name} - League {self.league} ({self.category})"