# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('registered_players', views.registered_players, name='registered_players'),
    path('registrations/', views.all_registrations_view, name='all_registrations'),
    path('registrations/download/', views.download_all_registrations_pdf, name='download_all_registrations_pdf'),
    path('fixture_view', views.fixture_view, name='fixture_view'),
]