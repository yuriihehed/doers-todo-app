from django import forms
from .models import ToDo, Team
from .models import Team

class TodoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['title', 'description', 'deadline', 'state', 'team']
        widgets = {
            'description': forms.Textarea(attrs={
                'cols': 55,  
                'rows': 5, 
                'class': 'description-box',  
            }),
        }
        
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
