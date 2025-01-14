from django.contrib import messages
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from datetime import timedelta
from .forms import TodoForm, TeamForm
from .models import Team, ToDo
from .forms import TodoForm

# User for testing purposes
user = User.objects.first()


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
            messages.success(request, 'You have registered successfully!')
            return redirect('register')
    return render(request, 'register.html')


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
            error = "Invalid email or password"  # set error message for failed login
    return render(request, 'login.html', {'error': error})  # render login page with error (if any)



# Registration Page
def registration_page(request):
    return render(request, 'registration.html')


# Forgot Password Page
def forgot_password(request):
    return render(request, 'forgot_password.html')


# renders the about page
def about_page(request):
    return render(request, "about.html", {"user": request.user})


# create team page
#@login_required
def create_team(request):
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        description = request.POST.get('description')
        
        if not team_name:
            messages.error(request, 'A team name is required.')
        
        
        # Save the new team to the database
        Team.objects.create(name=team_name, description=description, created_by=request.user)

        # Redirect to the teams list page
        return redirect('teams_list')

    # Render the create_team.html template
    return render(request, 'create_team.html')


# Teams Default View
def teams_default(request):
    first_team = Team.objects.first()
    if first_team:
        return redirect('team_details', id=first_team.id)
    else:
        messages.info(request, "No teams are available. Please create a new team.")
        return redirect('create_team')


# Team Details
# @login_required
        
        return redirect('teams_list')  # Redirect to teams list page
    return render(request, 'teamCreation.html', {'form': TeamForm()})

# list of all teams

def teams_list(request):
    teams = Team.objects.all()  # Fetch all teams
    return render(request, 'teams_list.html', {'teams': teams})

# team details page

def team_details(request, id):
    team = get_object_or_404(Team, id=id)
    if request.method == 'POST':
        new_member_email = request.POST.get('new_member')
        # Add logic to handle adding a new member
    return render(request, 'team_details.html', {'team': team})


# Teams List
def teams_list(request):
    teams = Team.objects.all()
    return render(request, 'teams_list.html', {'teams': teams})


# About Page
def about_page(request):
    return render(request, "about.html", {"user": request.user})


# Landing Page
def landing_page(request):
    return render(request, 'landing.html')


# Empty Dashboard
# @login_required
def dashboard_empty(request):
    return render(request, 'dashboardPage/dashboard_empty.html', {'user': request.user})


# Dashboard with Todos
# @login_required
def dashboard(request):
    todos = ToDo.objects.filter(user=request.user)
    if not todos.exists():
        return redirect('dashboard_empty')
    return render(request, 'dashboardPage/dashboard.html', {'todos': todos, 'user': request.user})


# Create Todo Item
# @login_required
def create_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('dashboard')
    else:
        form = TodoForm()
    return render(request, 'dashboardPage/create_todo.html', {'form': form})


# Update Todo State
# @login_required
def update_todo_state(request, todo_id, state):
    todo = get_object_or_404(ToDo, id=todo_id, user=request.user)
    todo.state = state
    todo.save()
    return redirect('dashboard')


# Delete Todo
# @login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id, user=request.user)
    todo.delete()
    return redirect('dashboard')
