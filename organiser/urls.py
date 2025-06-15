# urls.py

from django.urls import path
from .views import expenses

urlpatterns = [
    path('expenses/', expenses, name='expenses'),
]
