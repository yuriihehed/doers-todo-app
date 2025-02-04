from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from django import forms
from datetime import timedelta

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)  
    description = models.TextField(blank=True)  
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams')  
    created_at = models.DateTimeField(auto_now_add=True)  
    members = models.ManyToManyField(User, related_name='teams_joined', blank=True)  # Updated related_name

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_members')  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_membership')  # Updated related_name
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.team.name}"


############################################################################################################
#######################ToDo Model#######################################################################
class Category(models.Model):
    name = models.CharField(max_length=100)

    def str(self):
        return self.name
    
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
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='not_started')
    start_time = models.DateTimeField(null=True, blank=True)
    elapsed_time = models.DurationField(default=timedelta())
    last_active_time = models.DateTimeField(null=True, blank=True)

    # Team association
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='todos')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    assigned_user = models.ForeignKey(
    User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_todos"
)



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
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.none(),  # Start with an empty queryset
        required=True
    )

    class Meta:
        model = ToDo  # Link this form to the ToDo model
        fields = ['title', 'description', 'deadline', 'state', 'team', 'assigned_to']  
        # Specify the fields to be included in the form
        # These fields will correspond to the fields defined in the ToDo model

        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def init(self, args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get user before calling super
        super().init(args, **kwargs)
        if self.user:
           # Get teams where user is either a member or the creator
            self.fields['team'].queryset = Team.objects.filter(
                Q(members=self.user) | Q(created_by=self.user)).distinct()
            if 'team' in self.data:
                try:
                    team_id = int(self.data.get('team'))
                    team = Team.objects.get(id=team_id)
                    self.fields['assigned_to'].queryset = team.members.all()
                except (ValueError, Team.DoesNotExist):
                    pass
            elif self.instance.pk:
                self.fields['assigned_to'].queryset = self.instance.team.members.all()
