from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
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
            error = "Invalid email or password"
    return render(request, 'login.html', {'error': error})


# Registration Page
def registration_page(request):
    return render(request, 'registration.html')


# Forgot Password Page
def forgot_password(request):
    return render(request, 'forgot_password.html')


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
    return render(request, 'create_team.html')


# Teams Default View
def teams_default(request):
    # Get the first available team
    first_team = Team.objects.first()
    if first_team:
        # Render the team details page with the first team
        return render(request, 'team_details.html', {'team': first_team})
    else:
        # Redirect to create_team if no teams exist
        messages.info(request, "No teams are available. Please create a new team.")
        return redirect('create_team')


# Team Details
# @login_required
def team_details(request, id):
    try:
        # Ensure the team with the given ID exists
        team = Team.objects.get(id=id)
        if request.method == 'POST':
            new_member_email = request.POST.get('new_member')
            # Add logic to handle adding a new member
        return render(request, 'team_details.html', {'team': team})
    except Team.DoesNotExist:
        # If the team with the given ID does not exist, redirect to create_team
        messages.info(request, "Team not found. Please create a new team.")
        return redirect('create_team')
    except ValueError:
        # If the ID is invalid (not an integer), raise a 404 error
        raise Http404("Invalid team ID.")


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
    #
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

def teams_id(request):
    team_members = [
        {"id": "001", "name": "Gulbanu Madiyarova"},
        {"id": "002", "name": "Asad Bakhtiari"},
        {"id": "003", "name": "Kanchanjit Bandesha"},
        {"id": "004", "name": "Vanessa Wartemberg"},
        {"id": "005", "name": "Yurii Hehediush"},
        {"id": "006", "name": "John Le"},
    ]
    return render(request, 'teams_id.html', {"team_members": team_members})