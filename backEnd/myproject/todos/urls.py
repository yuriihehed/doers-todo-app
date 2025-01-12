from django.urls import path
from . import views

urlpatterns = [

    path('dashboard/empty/', views.dashboard_empty, name='dashboard_empty'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('landing/', views.landing_page, name='landing'),
    path('about/', views.about_page, name='about'),  
    #path('about/', views.about, name='about'),
]