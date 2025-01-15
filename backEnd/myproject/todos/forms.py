from django import forms
from .models import ToDo, Team

class TodoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['title', 'description', 'deadline', 'state']
        
class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description']
        error_messages = {
            'name': {
                "required": "A team name is required.",
                'unique': 'A team with that name already exists.'
            }
        }
