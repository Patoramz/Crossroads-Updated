"""Defines URL patterns for learning_logs"""
from django.urls import path
from . import views
app_name = 'silk'
urlpatterns = [

    # Home Page
    path('', views.index, name='index'),
    path('story/', views.create_character, name='story'),
    path('game/', views.game_view, name='game'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.custom_logout, name='logout'),
    ]
