from django.urls import path
from . import views

urlpatterns = [
    path('pay/<int:registration_id>/', views.initiate_payment, name='initiate_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),

]
