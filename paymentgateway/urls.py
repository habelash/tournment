from django.urls import path
from . import views

urlpatterns = [
    path('payment/<int:registration_id>/', views.initiate_payment, name='initiate_payment'),
    path('payment/<int:registration_id>/response', views.payment_response, name='payment_response'),
]
