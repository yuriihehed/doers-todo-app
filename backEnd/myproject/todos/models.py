from django.db import models
from django.contrib.auth.models import User

# Team model to represent a team
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)  # team name
    description = models.TextField(blank=True)  # optional description
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teams')  # creator of the team
    created_at = models.DateTimeField(auto_now_add=True)  # timestamp when the team was created

    def __str__(self):
        return self.name

# TeamMember model to represent members of a team
class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')  # reference to the team
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_members')  # reference to the user
    joined_at = models.DateTimeField(auto_now_add=True)  # timestamp when the user joined the team

    class Meta:
        unique_together = ('team', 'user')  # ensure a user cannot be added to the same team multiple times

# ToDo model to represent tasks
class ToDo(models.Model):
    title = models.CharField(max_length=255)  # title of the task
    description = models.TextField()  # description of the task
    state = models.CharField(max_length=255)  # state of the task (e.g., Pending, Completed)
    elapsed_time = models.DurationField()  # time taken for the task
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # user who owns the task

    def __str__(self):
        return self.title