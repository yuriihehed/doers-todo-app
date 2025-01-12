from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # root url
    path('login/', views.login_page, name='login'),  # login page
    path('dashboard/', views.home, name='dashboard'),  # dashboard page
    path('forgot-password/', views.forgot_password, name='forgot_password'),  # forgot password page
    path('registration/', views.registration_page, name='registration'),  # registration page
    path('teams/', views.teams_list, name='teams_list'),  # list of all teams
    path('teams/<int:id>/', views.team_details, name='team_details'),  # team details page with dynamic ID
]