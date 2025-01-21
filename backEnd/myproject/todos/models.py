from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from django import forms
from datetime import timedelta
from django.conf import settings
from django.db.models import Q  # Add this import

# Team model to represent a team
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams')
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='TeamMember',
        related_name='member_teams'  # Changed this
    )

    def __str__(self):
        return self.name

# TeamMember model to represent members of a team
class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_memberships')  # Changed this
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_memberships')  # Changed this
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.team.name}"

# Remove the duplicate 'name' field from TeamMember as it's redundant with user information

class ToDo(models.Model):
    STATE_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('stopped', 'Stopped')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='stopped')
    start_time = models.DateTimeField(null=True, blank=True)
    elapsed_time = models.DurationField(default=timedelta())
    last_active_time = models.DateTimeField(null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

    def is_overdue(self):
        return self.deadline and self.deadline < timezone.now()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'todos_todo'

class TodoForm(forms.ModelForm):
    team = forms.ModelChoiceField(
        queryset=Team.objects.none(),  # Start with empty queryset
        required=False,
        empty_label="No team selected"
    )

    class Meta:
        model = ToDo
        fields = ['title', 'description', 'deadline', 'state', 'team']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get user before calling super
        super().__init__(*args, **kwargs)
        if self.user:
            # Get teams where user is either a member or the creator
            self.fields['team'].queryset = Team.objects.filter(
                Q(members=self.user) | Q(created_by=self.user)
            ).distinct()