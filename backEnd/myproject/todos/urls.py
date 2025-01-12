from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.home, name='dashboard'),
    path('register/', views.register, name='register'), # for the register page 
]