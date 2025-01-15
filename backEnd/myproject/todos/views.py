from django.contrib import messages
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import timedelta
from .forms import TodoForm, TeamForm
from .models import Team, ToDo
from .forms import TodoForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required


#########################################################################################################################################################################
############ Landing Views ##############################################################################################################################################
#########################################################################################################################################################################
# Landing Page
def landing_page(request):
    return render(request, 'landing.html')

#########################################################################################################################################################################
############ About Views ################################################################################################################################################
#########################################################################################################################################################################
# About Page
def about_page(request):
    return render(request, "about.html", {"user": request.user})

#########################################################################################################################################################################
############ Dashboard Views ############################################################################################################################################
#########################################################################################################################################################################
# Empty Dashboard
@login_required
def dashboard_empty(request):
    return render(request, 'dashboardPage/dashboard_empty.html', {'user': request.user})

# Dashboard with Todos
@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login.html')  # Replace 'login' with the actual name of your login URL

    todos = ToDo.objects.filter(user=request.user).order_by('deadline')
    if not todos.exists():
        return redirect('dashboard_empty')
    return render(request, 'dashboard.html', {'todos': todos})

#########################################################################################################################################################################
############ Account Views ##############################################################################################################################################
#########################################################################################################################################################################
# User Registration
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm')

        if not email or not password or not confirm_password:
            messages.error(request, 'All fields are required.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            try:
                validate_email(email)
                user = User.objects.create_user(username=email, email=email, password=password)
                user.save()
                messages.success(request, 'You have registered successfully!')
                return redirect('register')
            except ValidationError:
                messages.error(request, 'Invalid email address.')
    return render(request, 'accountPage/register.html')

# Login Page
def login_page(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid email or password"
    return render(request, 'accountPage/login.html', {'error': error})

# Registration Page
def registration_page(request):
    return render(request, 'accountPage/registration.html')

# Forgot Password Page
def forgot_password(request):
    return render(request, 'accountPage/forgot_password.html')

# Logout Page
def logout_user(request):
    if request.method == 'POST':  # Handle the form submission for logout confirmation
        logout(request)  # Logs out the user
        return redirect(request, 'landing.html')  # Redirect to a landing page or login page after logout
    else:  # Display the logout confirmation page
        return render(request, 'accountPage/logout.html', {'user': request.user})

#########################################################################################################################################################################
############ Todos Views ################################################################################################################################################
#########################################################################################################################################################################

# Create Todo Item
@login_required
def create_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('dashboard')  # Adjust to your dashboard or desired page
    else:
        form = TodoForm()
    return render(request, 'todoPage/create_todo.html', {'form': form})

# Update Todo State
@login_required
def update_todo_state(request, todo_id, state):
    todo = get_object_or_404(ToDo, id=todo_id, user=request.user)
    todo.state = state
    todo.save()
    return redirect('dashboard')

# Delete Todo
@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id, user=request.user)
    todo.delete()
    return redirect('dashboard')

def teams_id(request):
    team_members = [
       {"id": "002", "name": "Asad Bakhtiari"},
    {"id": "003", "name": "Kanchanjit Bandesha"},
       {"id": "004", "name": "Vanessa Wartemberg"},
       {"id": "005", "name": "Yurii Hehediush"},
       {"id": "006", "name": "John Le"},
    ]
    return render(request, 'teamsPage/teams_id.html', {"team_members": team_members})

#########################################################################################################################################################################
############ Teams Views ################################################################################################################################################
#########################################################################################################################################################################

# Create Team Page
@login_required
def create_team(request):
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        description = request.POST.get('description')

        # Save the new team to the database
        Team.objects.create(name=team_name, description=description, created_by=request.user)
        # Redirect to the teams list page
        return redirect('teams_list')

    # Render the create_team.html template
    return render(request, 'teamCreation.html')

# Teams Default View
@login_required
def teams_default(request):
    # Filter teams created by the logged-in user
    user_teams = Team.objects.filter(created_by=request.user)
    if user_teams.exists():
        # Redirect to the first team's details page
        first_team = user_teams.first()
        return redirect('team_details', id=first_team.id)
    else:
        # Redirect to create_team if no teams exist
        messages.info(request, "No teams are available. Please create a new team.")
        return redirect('create_team')

# Team Details
@login_required
def team_details(request, id):
    try:
        # Get the specific team for the given ID
        team = Team.objects.get(id=id, created_by=request.user)
        if request.method == 'POST':
            # Add a new member if submitted
            new_member_email = request.POST.get('new_member')
            if new_member_email:
                # Add logic for adding the new member to the team
                messages.success(request, f"{new_member_email} added to the team.")
                # Add to database logic here if needed

        return render(request, 'teamsPage/team_details.html', {'team': team})
    except Team.DoesNotExist:
        messages.info(request, "Team not found. Please create a new team.")
        return redirect('create_team')

# Teams List
@login_required
def teams_list(request):
    teams = Team.objects.all()

    return render(request, 'teamsPage/teams_list.html', {'teams': teams})

#########################################################################################################################################################################
############ END ########################################################################################################################################################
#########################################################################################################################################################################
