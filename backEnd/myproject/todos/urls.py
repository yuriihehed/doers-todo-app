from django.urls import path, include
from . import views
# from .views import CustomLoginView

urlpatterns = [

    path('dashboardPage/empty/', views.dashboard_empty, name='dashboard_empty'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/create/', views.create_todo, name='create_todo'),

    path('update/<int:todo_id>/<str:state>/', views.update_todo_state, name='update_todo_state'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('todos/edit/<int:todo_id>/', views.edit_todo, name='edit_todo'),

    path('', views.landing_page, name='landing'),

    path('about/', views.about_page, name='about'),

    path('register/', views.register, name='register'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),  # forgot password page NOT CONNECT TO ANYTHING YET
    path('registration/', views.registration_page, name='registration'),  # registration page NEED TO BE CONNECT TO REGISTRATION
    path('accounts/', include('django.contrib.auth.urls')),  # Add this line if not already present
    path('login/', views.login_page, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('logout/', views.logout_user, name='logout'),
    
    path('teams/new/', views.create_team, name='create_team'),  # Updated path for "Create Team"
    path('teams/', views.teams_default, name='teams_default'),
    path('teams_list/', views.teams_list, name='teams_list'),
    path('teams/id/', views.teams_id, name='teams_id'),
    path('accounts/', include('django.contrib.auth.urls')),  # Add this line if not already present

    path('todos/new/', views.create_todo, name='create_todo'),  # Create ToDo page
    path('todos/<int:todo_id>/update/<str:state>/', views.update_todo_state, name='update_todo_state'),  # Update state
    path('todos/<int:todo_id>/delete/', views.delete_todo, name='delete_todo'),  # Delete ToDo
    path('teams/', views.teams_id, name='teams_id'),  # Teams dropdown
    
    path('update_todo_state/<int:todo_id>/<str:new_state>/', views.update_todo_state, name='update_todo_state'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
]

