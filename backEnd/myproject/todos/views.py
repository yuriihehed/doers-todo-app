from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Team

# renders dashboard page
def home(request):
    return render(request, 'dashboard.html')

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

# registration page
def registration_page(request):
    return render(request, 'registration.html')  # show registration page

# forgot password page
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
#@login_required
def teams_list(request):
    teams = Team.objects.all()  # Fetch all teams
    return render(request, 'teams_list.html', {'teams': teams})

## team details page
#@login_required
def team_details(request, id):
    team = get_object_or_404(Team, id=id)  # Get the team by ID or return a 404
    return render(request, 'team_details.html', {'team': team})