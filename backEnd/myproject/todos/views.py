from django.contrib import messages
from django.db import IntegrityError, models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import timedelta
from .forms import TodoForm, TeamForm
from .models import Team, ToDo, TeamMember
from .forms import TodoForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone




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
        return redirect('login')

    state_filter = request.GET.get('category', '')  
    team_id = request.GET.get('team', '')

    all_todos = ToDo.objects.filter(user=request.user)  
    if not all_todos.exists():
        return redirect('dashboard_empty')  

    todos = all_todos.select_related('team').order_by('deadline')

    if state_filter:
        todos = todos.filter(state=state_filter)

    if team_id:
        todos = todos.filter(team_id=team_id)

    teams = Team.objects.all()  # Fetch all teams for the dropdown

    return render(request, 'dashboardPage/dashboard.html', {
        'todos': todos,  
        'teams': teams
    })

#########################################################################################################################################################################
############ Account Views ##############################################################################################################################################
#########################################################################################################################################################################
# User Registration
def register(request):


   if request.method == 'POST': # if the request method is POST


       # then get the form data from the POST request
       email = request.POST.get('email')
       password = request.POST.get('password')
       confirm_password = request.POST.get('confirm')


       # initialize an empty dictionary to store any errors
       errors = {}


       # check if the email field, password field, and confirm password field are empty
       if not email:
           errors['email'] = 'Email is required.'
       if not password:
           errors['password'] = 'Password is required.'
       if not confirm_password:
           errors['confirm'] = 'Please confirm your password.'


        # check if the passwords match
       if password and confirm_password and password != confirm_password:
           errors['confirm'] = 'Passwords do not match.'


       # check if the email is valid
       if email:
           try:
               # validate the email
               validate_email(email)
               # check if the email is already in use
               if User.objects.filter(email=email).exists():
                   errors['email'] = 'Email is already in use.'
           except ValidationError:
               errors['email'] = 'Invalid email address.'


       # if there are validation errors, rerender the form with the errors
       if errors:
           return render(request, 'accountPage/register.html', {'errors': errors, 'email': email})
      
       # if no errors, create the user
       user = User.objects.create_user(email, email, password)
       user.save()
       messages.success(request, 'Account created successfully.')
       return redirect('login')  # Redirect to the login page
  
   # if the request is GET, render the registration page
   return render(request, 'accountPage/register.html')




# Login Page
def login_page(request):
   error = None
   # Check if the form is submitted and get the arguments
   if request.method == 'POST':
       email = request.POST.get('email')
       password = request.POST.get('password')


       # Authenticate the user
       user = authenticate(request, username=email, password=password)
       if user:
           # If the user is authenticated, log them in
           login(request, user)
           return redirect('dashboard')
       else:
           # If the user is not authenticated, display an error message
           error = "Invalid email or password"
   return render(request, 'accountPage/login.html', {'error': error})


# Registration Page
def registration_page(request):
   return render(request, 'accountPage/registration.html')


# Forgot Password Page
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        errors = {}

        if not email:
            errors['email'] = 'Email is required.'
        else:
            if not User.objects.filter(email=email).exists():
                errors['email'] = 'Email does not exist in our system.'

        if errors:
            return render(request, 'accountPage/forgot_password.html', {'errors': errors, 'email': email})

        # Here you would typically send a password reset email
        messages.success(request, 'Password reset instructions have been sent to your email.')
        return redirect('login')
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
def get_team_members(request, team_id):
    users = Team.objects.all()  
    members_data = [{'id': user.id, 'username': user.username} for user in users]
    return JsonResponse({'members': members_data})

def get_team_members(request, team_id):
    users = User.objects.all()  
    members_data = [{'id': user.id, 'username': user.username} for user in users]
    return JsonResponse({'members': members_data})

@login_required
# Create Todo Item
def create_todo(request):

    # Handle POST request
    if request.method == 'POST':  
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)  # Do not save yet

            # Assign the current user as the creator
            todo.user = request.user  

            # Get selected team from form
            team_id = request.POST.get('team')
            if team_id:
                todo.team = get_object_or_404(Team, id=team_id)

            # Get selected assigned user from form
            assigned_user_id = request.POST.get('assigned_to')
            if assigned_user_id:
                assigned_user = get_object_or_404(User, id=assigned_user_id)
                todo.assigned_user = assigned_user  # Set assigned user
            else:
                todo.assigned_user = request.user  # Default to the current user if no one is selected

            todo.save()  # Save to database
            messages.success(request, "ToDo created successfully.")
            return redirect('dashboard')

    else:
        form = TodoForm()
    teams = Team.objects.all()

    return render(request, 'todoPage/create_todo.html', {'form': form, 'teams': teams})






# View User's Todos
@login_required
def user_todos(request):
   todos = ToDo.objects.filter(user=request.user) 
   # Query the database to get all ToDo items for the logged-in user
   return render(request, 'dashboardPage/dashboard.html', {'todos': todos}) 
   # Render the 'dashboard.html' template, passing the user's ToDos as context


login_required
def get_timer(request, todo_id):
   todo = get_object_or_404(ToDo, id=todo_id, user=request.user)
   elapsed = todo.elapsed_time
  
   # If todo is active, add the time since last_active_time
   if todo.state == 'active' and todo.last_active_time:
       current_elapsed = timezone.now() - todo.last_active_time
       elapsed += current_elapsed
  
   # Convert to total seconds
   total_seconds = int(elapsed.total_seconds())
  
   # Format as 00h00m00s
   hours = total_seconds // 3600
   minutes = (total_seconds % 3600) // 60
   seconds = total_seconds % 60
  
   formatted_time = f"{hours:02d}h{minutes:02d}m{seconds:02d}s"
  
   return JsonResponse({'elapsed_time': formatted_time})


#update todo state
@login_required
def update_todo_state(request, todo_id, new_state):
   todo = get_object_or_404(ToDo, id=todo_id, user=request.user)
   old_state = todo.state
   todo.state = new_state


   current_time = timezone.now()


   if old_state == 'active' and new_state in ['stopped', 'paused']:
       if todo.last_active_time:
           elapsed = current_time - todo.last_active_time
           todo.elapsed_time += elapsed


   if new_state == 'active':
       todo.last_active_time = current_time


   todo.save()
   return redirect('dashboard')
# View for deleting a ToDo
def delete_todo(request, todo_id):
   todo = get_object_or_404(ToDo, pk=todo_id, user=request.user)
   todo.delete()
   return redirect('dashboard')  # Redirect back to the dashboard
# View for editing a ToDo

@login_required
def edit_todo(request, todo_id):
    todo = get_object_or_404(ToDo, pk=todo_id, user=request.user)
    
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            # Save the form but do NOT commit yet
            todo = form.save(commit=False)

            # Retrieve assigned user from the form submission
            assigned_user_id = request.POST.get('assigned_to')
            if assigned_user_id:
                assigned_user = get_object_or_404(User, id=assigned_user_id)
                todo.assigned_user = assigned_user  # Set assigned user
            else:
                todo.assigned_user = None  # Clear assigned user if none selected

            todo.save()  # Now save to DB with the assigned user
            messages.success(request, "ToDo updated successfully.")
            return redirect('dashboard')

    else:
        form = TodoForm(instance=todo)

    teams = Team.objects.all()
    team_members = TeamMember.objects.filter(team=todo.team) if todo.team else []
    
    return render(request, 'todoPage/edit_todo.html', {
        'form': form,
        'todo': todo,
        'user_email': request.user.email,
        'teams': teams,
        'team_members': team_members,
        'assigned_user': todo.assigned_user,  # Ensure assigned_user is passed
    })
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



@login_required
# Check if the logged-in user has created a team
def team_context(request):
   if not request.user.is_authenticated:
       return redirect('login')  # Redirect to the login page if the user is not logged in
   teams_exist = Team.objects.filter(created_by=request.user).exists()
   if not teams_exist:
       return redirect('create_team')
   return redirect('teams_list')  # Redirect to the teams list if the user has created a team


# Create Team Page
@login_required
def create_team(request):
    error_team_name = None
    error_description = None
    error_member_email = None
    team_name = ""
    description = ""
    team_member_email = ""

    if request.method == 'POST':
        team_name = request.POST.get('team_name', '').strip()
        description = request.POST.get('description', '').strip()
        team_member_email = request.POST.get('team_member_email', '').strip()

        # Validation
        if not team_name:
            error_team_name = "Team Name is required."
        elif Team.objects.filter(name=team_name).exists():
            error_team_name = "A team with this name already exists."

        if not description:
            error_description = "Description is required."

        # If no errors, proceed to create the team
        if not error_team_name and not error_description:
            try:
                team = Team.objects.create(name=team_name, description=description, created_by=request.user)
                
                TeamMember.objects.create(team=team, user=request.user)  # Add the creator as a team member

                # Check if the user exists
                user = User.objects.filter(email=team_member_email).first()

                if user:
                    # Create a TeamMember entry to link the user to the team
                    team_member, created = TeamMember.objects.get_or_create(team=team, user=user)

                    messages.success(request, f"Team '{team_name}' created successfully, and '{user.email}' was added as a member.")
                else:
                    error_member_email = "No user found with this email."

                # Redirect to the team details page after creation
                return redirect('teams_list')

            except IntegrityError:
                error_team_name = "A team with this name already exists."

    return render(request, 'teamCreation.html', {
        'error_team_name': error_team_name,
        'error_description': error_description,
        'error_member_email': error_member_email,
        'team_name': team_name,
        'description': description,
        'team_member_email': team_member_email,
    })


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
   
@login_required
def team_details(request, id):
    errors = {}  # Initialize the error dictionary
    
    # Get the specific team for the given ID
    team = get_object_or_404(Team, id=id)
    team_members = TeamMember.objects.filter(team=team)

    if request.method == 'POST':
        # Get the new member's username or email from the form
        new_member_name = request.POST.get('new_member', '').strip()

        # Validation checks
        if not new_member_name:
            errors['new_member'] = "Member name is required."
        else:
            # Try to find the user by username or email
            user = User.objects.filter(username=new_member_name).first()

            if not user:
                user = User.objects.filter(email=new_member_name).first()
            
            if not user:
                errors['new_member'] = "User does not exist."
                
            else:
                # Check if the user is already in the team
                if team.team_members.filter(user=user).exists():
                    errors['new_member'] = "This member is already in the team."
                else:
                    # Add the new member to the team
                    new_member, created = TeamMember.objects.get_or_create(team=team, user=user)
                    messages.success(request, f"'{user.username}' added to the team.")
                    
    # Render the team details template
    return render(request, 'teamsPage/team_details.html', {'team': team,'team_members': team_members, 'errors': errors})


# Teams List
def teams_list(request):
    teams = Team.objects.all()

    # Create a list of teams where the user is either the owner or a member
    user_teams = [
        team for team in teams if team.created_by == request.user or team.team_members.filter(user=request.user).exists()
    ]

    # Optionally, sort teams by created date or name
    user_teams.sort(key=lambda team: team.created_at, reverse=True)  # Sort by creation date (most recent first)

    return render(request, 'teamsPage/teams_list.html', {'teams': user_teams})

#########################################################################################################################################################################
############ END ########################################################################################################################################################
#########################################################################################################################################################################

@login_required
###### TYRING TO ADD new edit and delete for teams_list.html
# used for team_list html to edit team
def edit_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)  # Fetch the specific team
    if request.method == "POST":
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()  # Save the updated team
            return redirect('teams_list')  # Redirect to the list of teams
    else:
        form = TeamForm(instance=team)  # Pre-fill the form with the team's data
    return render(request, 'teamsPage/edit_team.html', {'form': form, 'team': team})


@login_required
# I want to make a function call edit_teammember for the team_details page 
def edit_teammember(request, team_id, member_id):
    team = get_object_or_404(Team, id=team_id, created_by=request.user)  # Fetch the team
    member = get_object_or_404(TeamMember, id=member_id, team=team)  # Fetch the team member

    if request.method == "POST":
        updated_email = request.POST.get('email')  # Get updated email from form

        if updated_email:
            # Ensure no duplicate emails exist before updating
            if User.objects.exclude(id=member.user.id).filter(email=updated_email).exists():
                messages.error(request, "This email is already in use by another member.")
            else:
                member.user.email = updated_email  # Update user's email
                member.user.save()  # Save user model update
                messages.success(request, f"Member '{member.user.username}' updated successfully.")
                return redirect('team_details', id=team_id)  # Redirect to the team details

    # Render a simple form for editing the member's email
    return render(request, 'teamsPage/edit_member.html', {'member': member, 'team': team})

@login_required
# used for team_list html to delete teammember
def delete_teammember(request, team_id, member_id):
    team = get_object_or_404(Team, id=team_id, created_by=request.user)  # Fetch the team
    member = get_object_or_404(TeamMember, id=member_id, team=team)  # Fetch the team member

    if request.method == "POST":
        member_email = member.user.email  # Get the member's email before deletion
        member.delete()  # Correctly delete the TeamMember entry

        messages.success(request, f"Member '{member_email}' removed from the team.")
        return redirect('team_details', id=team_id)  # Redirect back to the team details page

    return redirect('team_details', id=team_id)  # Redirect to the list of teams
    
    #return render(request, 'confirm_delete.html', {'team': team})   <--- This is a confirm delete page that I need to create

@login_required
# used for team_list html to delete team
def delete_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)  # Fetch the specific team
    if request.method == "POST":
        team.delete()  # Delete the team
        return redirect('teams_list')  # Redirect to the list of teams
    return render(request, 'confirm_delete.html', {'team': team})
