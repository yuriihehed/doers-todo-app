from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from django import forms
from datetime import timedelta


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

class ToDo(models.Model):
    STATE_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('stopped', 'Stopped'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) 
    deadline = models.DateField(null=True, blank=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='stopped') 
    start_time = models.DateTimeField(null=True, blank=True)  # Track when the timer started
    elapsed_time = models.DurationField(default="0")  # Store as timedelta
    last_active_time = models.DateTimeField(null=True, blank=True)

    def is_overdue(self):
        return self.deadline and self.deadline < timezone.now()
    
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'todos_todo'


class TodoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['title', 'description', 'deadline', 'state']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
