from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import timedelta
#from .models import Todo 

def about_page(request):
    return render(request, "about.html", {"user": request.user})

# Create your views here.
def landing_page(request):
    return render(request, 'landing.html')

#def about(request):
 #   return render(request, 'about.html')
#@login_required
def dashboard_empty(request):
    return render(request, 'dashboardPage/dashboard_empty.html', {'user': request.user})

#@login_required
#Todo.objects.filter(user=request.user)
def dashboard(request):
    todos = [
       {'title': 'Sample ToDo 1', 'description': 'Description 1', 'state': 'stopped', 'elapsed_time': timedelta(hours=1, minutes=30)},
       {'title': 'Sample ToDo 2', 'description': 'Description 2', 'state': 'paused', 'elapsed_time': timedelta(hours=0, minutes=45)},
       {'title': 'Sample ToDo 3', 'description': 'Description 3', 'state': 'active', 'elapsed_time': timedelta(hours=2, minutes=15)},
]
    return render(request, 'dashboardPage/dashboard.html', {'todos': todos, 'user': request.user})