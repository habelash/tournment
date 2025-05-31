from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_tournament, name='tournament_register'),
    path('', views.home, name='home'),
]
