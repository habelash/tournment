from django.contrib import admin
from .models import LeagueAssignment
from registration.models import TournamentRegistration
from .utils import reshuffle_leagues
from django.contrib import messages


@admin.register(LeagueAssignment)
class LeagueAssignmentAdmin(admin.ModelAdmin):
    list_display = ('team', 'league', 'category')
    actions = ['refresh_league_assignments']

    def refresh_league_assignments(self, request, queryset):
        reshuffle_leagues()
        self.message_user(request, "✅ Leagues reshuffled successfully!", messages.SUCCESS)

    refresh_league_assignments.short_description = "🔁 Refresh League Assignments"
