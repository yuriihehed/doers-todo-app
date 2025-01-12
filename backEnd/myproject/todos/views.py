from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.
def home(request):
    return render(request, 'dashboard.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm')

        # Validate the form inputs
        if not email or not password or not confirm_password:
            messages.error(request, 'All fields are required.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            # user registration (e.g., save to the database)
            messages.success(request, 'You have registered successfully!')
            return HttpResponseRedirect('/register/')

    # Render the registration template
    return render(request, 'register.html')
