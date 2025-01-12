from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=100)  # team name
    description = models.TextField(blank=True)  # optional description
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teams')  # creator of the team
    created_at = models.DateTimeField(auto_now_add=True)  # timestamp when the team was created

class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')  # reference to the team
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_members')  # reference to the user
    joined_at = models.DateTimeField(auto_now_add=True)  # timestamp when the user joined the team

    class Meta:
        unique_together = ('team', 'user')  # ensure a user cannot be added to the same team multiple times