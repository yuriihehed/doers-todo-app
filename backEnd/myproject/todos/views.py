from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import timedelta
from .models import Team, ToDo
from .forms import TodoForm

# handles login page
def login_page(request):
    error = None
    if request.method == 'POST':  # only process POST requests
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # redirect to dashboard if login successful
        else:
            error = "Invalid email or password"  # set error message for failed login
    return render(request, 'loginpage.html', {'error': error})  # render login page with error (if any)

# renders the registration page
def registration_page(request):
    return render(request, 'registration.html')  # show registration page

# renders the forgot password page
def forgot_password(request):
    return render(request, 'forgot_password.html')  # show forgot password page

# create team page
@login_required
def create_team(request):
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        description = request.POST.get('description')
        
        # Save the new team to the database
        Team.objects.create(name=team_name, description=description, created_by=request.user)
        
        return redirect('teams_list')  # Redirect to teams list page
    return render(request, 'teams.html', {'user_email': request.user.email})

# list of all teams
@login_required
def teams_list(request):
    teams = Team.objects.all()  # Fetch all teams
    return render(request, 'teams_list.html', {'teams': teams})

# team details page
@login_required
def team_details(request, id):
    team = get_object_or_404(Team, id=id)  # Get the team by ID or return a 404
    return render(request, 'team_details.html', {'team': team})

# renders the about page
def about_page(request):
    return render(request, "about.html", {"user": request.user})

# renders the landing page
def landing_page(request):
    return render(request, 'landing.html')

# renders an empty dashboard page if no data exists
@login_required
def dashboard_empty(request):
    return render(request, 'dashboardPage/dashboard_empty.html', {'user': request.user})

# renders the dashboard page with todos
@login_required
def dashboard(request):
    todos = ToDo.objects.filter(user=request.user)
    if not todos.exists():
        return redirect('dashboard_empty')  # Redirect to empty dashboard if no todos
    return render(request, 'dashboardPage/dashboard.html', {'todos': todos, 'user': request.user})

# create a new todo item
@login_required
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

# update the state of a todo item
@login_required
def update_todo_state(request, todo_id, state):
    todo = get_object_or_404(ToDo, id=todo_id, user=request.user)
    todo.state = state
    todo.save()
    return redirect('dashboard')

# delete a todo item
@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id, user=request.user)
    todo.delete()
    return redirect('dashboard')