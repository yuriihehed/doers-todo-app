from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from django import forms
from datetime import timedelta

class Member(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# Team model to represent a team
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)  # team name
    description = models.TextField(blank=True)  # optional description
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teams')  # creator of the team
    created_at = models.DateTimeField(auto_now_add=True)  # timestamp when the team was created
    members = models.ManyToManyField(Member, related_name='teams')

    def __str__(self):
        return self.name
    
# TeamMember model to represent members of a team
class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_members')  # reference to the team
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_members')  # reference to the user
    joined_at = models.DateTimeField(auto_now_add=True)  # timestamp when the user joined the team

    class Meta:
        unique_together = ('team', 'user')  # ensure a user cannot be added to the same team multiple times


############################################################################################################
#######################ToDo Model#######################################################################

class ToDo(models.Model):  # Define a model for a ToDo item, representing a task in your app
    # A set of predefined choices for the state of the task
    STATE_CHOICES = [
        ('not_started', 'Not Started'),  
        ('in_progress', 'In Progress'),  
        ('completed', 'Completed'),
        ('completed', 'Completed'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('stopped', 'Stopped')  
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
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='todos') # Reference to the Team

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

    # Methods for the ToDo model
    def is_overdue(self):  
        # Checks if the task is overdue
        # Returns True if `deadline` exists and is in the past
        return self.deadline and self.deadline < timezone.now()

    def __str__(self):  
        # Returns a string representation of the ToDo instance
        # Used in admin panels or debugging to display the title of the ToDo
        return self.title

    class Meta:  
        # Meta options for the model
        db_table = 'todos_todo'  
        # Specifies the name of the database table for this model as 'todos_todo'


class TodoForm(forms.ModelForm):  # A form based on the ToDo model
    class Meta:
        model = ToDo  # Link this form to the ToDo model
        fields = ['title', 'description', 'deadline', 'state', 'team']  
        # Specify the fields to be included in the form
        # These fields will correspond to the fields defined in the ToDo model

        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            # Customize the `deadline` field to use a datetime-local input in the HTML form
        }
