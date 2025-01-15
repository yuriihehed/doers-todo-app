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
#@login_required
def dashboard_empty(request):
    return render(request, 'dashboardPage/dashboard_empty.html', {'user': request.user})

# Dashboard with Todos
#@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login.html')  # Replace 'login' with the actual name of your login URL

    todos = ToDo.objects.filter(user=request.user).order_by('deadline')
    if not todos.exists():
        return redirect('dashboard_empty')
    return render(request, 'dashboardPage/dashboard.html', {'todos': todos})

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
        return render(request, 'landing.html')  # Redirect to a landing page or login page after logout
    else:  # Display the logout confirmation page
        return render(request, 'accountPage/logout.html', {'user': request.user})

#########################################################################################################################################################################
############ Todos Views ################################################################################################################################################
#########################################################################################################################################################################

# Create Todo Item
@login_required
def create_todo(request):
    if request.method == 'POST':  # Check if the request is a POST request (form submission)
        form = TodoForm(request.POST)  # Bind the submitted data to the TodoForm
        if form.is_valid():  # Check if the form data is valid
            todo = form.save(commit=False)  # Create a ToDo object but don't save it to the database yet
            todo.user = request.user  # Assign the logged-in user as the owner of the ToDo
            todo.save()  # Save the ToDo to the database
            return redirect('dashboard')  # Redirect to the dashboard or list of user's ToDos
    else:  # If the request is not POST (likely a GET request)
        form = TodoForm()  # Create an empty form instance for the user to fill out
    return render(request, 'todoPage/create_todo.html', {'form': form})  
    # Render the 'create_todo.html' template with the empty or pre-filled form


# View User's Todos
@login_required
def user_todos(request):
    todos = ToDo.objects.filter(user=request.user)  
    # Query the database to get all ToDo items for the logged-in user
    return render(request, 'dashboardPage/dashboard.html', {'todos': todos})  
    # Render the 'dashboard.html' template, passing the user's ToDos as context

# Update Todo State
# @login_required
def update_todo_state(request, todo_id, state):
    todo = get_object_or_404(ToDo, id=todo_id, user=request.user)  
    # Retrieve the ToDo item by ID, ensuring it belongs to the logged-in user
    # If not found, return a 404 error
    todo.state = state  # Update the state of the ToDo
    todo.save()  # Save the updated state to the database
    return redirect('user_todos')  
    # Redirect the user back to their list of ToDos

# Delete Todo
# @login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id, user=request.user)  
    # Retrieve the ToDo item by ID, ensuring it belongs to the logged-in user
    # If not found, return a 404 error
    todo.delete()  # Delete the ToDo item from the database
    return redirect('user_todos')  
    # Redirect the user back to their list of ToDos after deletion


# Team Members (for dropdown menu in the form)
@login_required
def teams_id(request):
    team_members = [
       {"id": "002", "name": "Asad Bakhtiari"},
       {"id": "003", "name": "Kanchanjit Bandesha"},
       {"id": "004", "name": "Vanessa Wartemberg"},
       {"id": "005", "name": "Yurii Hehediush"},
       {"id": "006", "name": "John Le"},
    ]
    return render(request, 'todoPage/teams_id.html', {"team_members": team_members}) 

#########################################################################################################################################################################
############ Teams Views ################################################################################################################################################
#########################################################################################################################################################################

# Create Team Page
# @login_required
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
# @login_required
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
# @login_required
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
# @login_required
def teams_list(request):
    teams = Team.objects.all()

    return render(request, 'teamsPage/teams_list.html', {'teams': teams})

#########################################################################################################################################################################
############ END ########################################################################################################################################################
#########################################################################################################################################################################
