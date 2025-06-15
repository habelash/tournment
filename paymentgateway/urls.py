from django.urls import path
from . import views

urlpatterns = [
    path('pay/<int:registration_id>/', views.initiate_payment, name='initiate_payment'),
    path('payment_qr/<int:registration_id>/', views.payment_qr, name='payment_qr'),
    path('payment/upload/<int:registration_id>', views.upload_screenshot, name='upload_screenshot'),

]
