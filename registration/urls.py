from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_tournament, name='tournament_register'),
    path('return_policies/', views.return_policies, name='return_policies'),
    path('', views.home, name='home'),
]
