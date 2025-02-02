from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from django import forms
from datetime import timedelta

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_teams"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(
        User, related_name="teams_joined", blank=True
    ) 

    def str(self):
        return self.name


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="team_members"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="team_membership"
    )  
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("team", "user")

    def str(self):
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
   state = models.CharField(max_length=20, choices=STATE_CHOICES, default='stopped')
   start_time = models.DateTimeField(null=True, blank=True)
   elapsed_time = models.DurationField(default=timedelta())
   last_active_time = models.DateTimeField(null=True, blank=True)
   team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='todos') # Reference to the Team
   category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
   def is_overdue(self):
       return self.deadline and self.deadline < timezone.now()
  
   # Timestamp for when the ToDo was created. Automatically set when the ToDo is created.
   created_at = models.DateTimeField(auto_now_add=True) 
  
   # Optional deadline for completing the task. Can be left empty.
   deadline = models.DateTimeField(null=True, blank=True) 


    # The current state of the task. It uses predefined choices (STATE_CHOICES) and defaults to 'not_started'.
   state = models.CharField(
       max_length=20, choices=STATE_CHOICES, default='not_started'
   )
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
       model = ToDo  # Link this form to the ToDo model
       fields = ['title', 'description', 'deadline', 'state', 'team'] 
       # Specify the fields to be included in the form
       # These fields will correspond to the fields defined in the ToDo model


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


