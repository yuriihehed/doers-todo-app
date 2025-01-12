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
]