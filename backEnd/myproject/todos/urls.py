from django.urls import path
from . import views

urlpatterns = [

    path('dashboardPage/empty/', views.dashboard_empty, name='dashboard_empty'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/create/', views.create_todo, name='create_todo'),
    path('update/<int:todo_id>/<str:state>/', views.update_todo_state, name='update_todo_state'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('landing/', views.landing_page, name='landing'),
    path('about/', views.about_page, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),  # login page
    path('forgot-password/', views.forgot_password, name='forgot_password'),  # forgot password page NOT CONNECT TO ANYTHING YET
    path('registration/', views.registration_page, name='registration'),  # registration page NEED TO BE CONNECT TO REGISTRATION
    path('teams/', views.teams_list, name='teams_list'),  # list of all teams ONE OF THESE ( need to be addedt to the correct teams_list)
    path('teams/<int:id>/', views.team_details, name='team_details'),  # team details page with dynamic ID need to be correct to team details
    path('teams/new/', views.create_team, name='create_team'),  # create team page need to be correct to create team
    path('teams/create/', views.create_team, name='create_team'),  # Correctly named pattern
    path('teams/', views.teams_default, name='teams_default'),
    path('teams_list/', views.teams_list, name='teams_list'),
]