from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView

# from .views import CustomLoginView

urlpatterns = [
    # Home Page
    path('', views.landing_page, name='landing'),
    
    # About Page
    path('about/', views.about_page, name='about'),
    
    # Login Page
    path('accounts/login/',views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),  # forgot password page NOT CONNECT TO ANYTHING YET
    path('registration/', views.registration_page, name='registration'),  # registration page NEED TO BE CONNECT TO REGISTRATION
    path('accounts/', include('django.contrib.auth.urls')),  # Add this line if not already present
    path('login/', views.login_page, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('logout/', views.logout_user, name='logout'),

    # Dashboard Page
    path('dashboardPage/empty/', views.dashboard_empty, name='dashboard_empty'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/create/', views.create_todo, name='create_todo'),
    path('get_timer/<int:todo_id>/', views.get_timer, name='get_timer'),


    path('update/<int:todo_id>/<str:state>/', views.update_todo_state, name='update_todo_state'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('todos/edit/<int:todo_id>/', views.edit_todo, name='edit_todo'),

    
    
    
    # Team Page
    path('teams/new/', views.team_context, name='team_context'),  # team context
    path('teams/new/creation/', views.create_team, name='create_team'),  # creating new team page
    path('teams/', views.teams_default, name='teams_default'),
    path('teams_list/', views.teams_list, name='teams_list'), # teams list page
    path('teams/id/', views.teams_id, name='teams_id'),
    
    path('accounts/', include('django.contrib.auth.urls')),  # Add this line if not already present

    path('todos/new/', views.create_todo, name='create_todo'),  # Create ToDo page
    path('<int:todo_id>/update/<str:state>/', views.update_todo_state, name='update_todo_state'),
    path('todos/<int:todo_id>/delete/', views.delete_todo, name='delete_todo'),  # Delete ToDo
    path('teams/', views.teams_id, name='teams_id'),  # Teams dropdown
    
    path('update_todo_state/<int:todo_id>/<str:new_state>/', views.update_todo_state, name='update_todo_state'),

    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),

    path('teams/<int:id>/', views.team_details, name='team_details'),  # Define URL for team_details view

    path('teams/<int:team_id>/delete/', views.delete_team, name='delete_team'), 
    path('teams/<int:team_id>/edit/', views.edit_team, name='edit_team'),

    # path('teams/<int:team_id>/add_member/', views.add_member, name='add_member'),
]

