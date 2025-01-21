from django import forms
from .models import ToDo, Team
from .models import Team, Member

class TodoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['title', 'description', 'deadline', 'state']
        
class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description', 'members']
        
        members = forms.ModelMultipleChoiceField(
            queryset= Member.objects.all(),
            widget=forms.CheckboxSelectMultiple,  # Or use `forms.SelectMultiple` for a multi-select dropdown
            required=False)
        error_messages = {
            'name': {
                "required": "A team name is required.",
                'unique': 'A team with that name already exists.'
            }
        }
