from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import timedelta
from .models import ToDo
from .forms import TodoForm 
user = User.objects.first() # Get the first user in the database for testing purposes
def about_page(request):
    return render(request, "about.html", {"user": request.user})

def landing_page(request):
    return render(request, 'landing.html')

#@login_required
def dashboard_empty(request):
    #return render(request, 'dashboardPage/dashboard_empty.html', {'user': request.user})
    return render(request, 'dashboardPage/dashboard_empty.html', {'user': user})

#Dashboard
#@login_required
def dashboard(request):
    # Hardcode a user for testing purposes
    user = User.objects.first()  # Get the first user in the database
    #todos = ToDo.objects.filter(user=request.user) removed for testing purposes
    todos = ToDo.objects.filter(user=user)
    if not todos.exists():
        return redirect('dashboard_empty')
    #return render(request, 'dashboardPage/dashboard.html', {'todos': todos, 'user': request.user})
    return render(request, 'dashboardPage/dashboard.html', {'todos': todos, 'user': user})

##@login_required
def create_todo(request):
    # Hardcode a user for testing purposes
    user = User.objects.first()  # Get the first user in the database
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            #todo.user = request.user removed for testing purposes
            todo.user = user
            todo.save()
            return redirect('dashboard')
        else:
            form = TodoForm()
        return render(request, 'dashboardPage/create_todo.html', {'form': form})
    
#Dashboard
# #@login_required
def update_todo_state(request, todo_id, state):
    # Hardcode a user for testing purposes
    user = User.objects.first()  # Get the first user in the database
    #todo = get_object_or_404(ToDo, id=todo_id, user=request.user) removed for testing purposes
    todo = get_object_or_404(ToDo, id=todo_id, user=user)
    todo.state = state
    todo.save()
    return redirect('dashboard')

#Dashboard
#@login_required
def delete_todo(request, todo_id):
    # Hardcode a user for testing purposes
    user = User.objects.first()  # Get the first user in the database
    #todo = get_object_or_404(ToDo, id=todo_id, user=request.user) removed for testing purposes
    todo = get_object_or_404(ToDo, id=todo_id, user=user)
    todo.delete()
    return redirect('dashboard')