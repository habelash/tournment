from django.shortcuts import render, redirect
from .registrationform import TournamentRegistrationForm
from .models import TournamentRegistration
from paymentgateway.views import initiate_payment
from paytmchecksum import PaytmChecksum
from django.views.decorators.csrf import csrf_exempt 
from django.shortcuts import get_object_or_404
# Create your views here.

def register_tournament(request):
    if request.method == "POST":
        player_name = request.POST.get("player_name")
        phone_number = request.POST.get("phone_number")
        player_email = request.POST.get("player_email")
        partner_name = request.POST.get("partner1_name")
        partner_phone_number = request.POST.get("partner1_phone")
        partner_email = request.POST.get("partner1_email")
        partner_2_name = request.POST.get("partner2_name")
        partner_2_number = request.POST.get("partner2_phone")
        partner_2_email = request.POST.get("partner2_email")
        category = request.POST.get("category")

        # Save registration immediately
        registration = TournamentRegistration.objects.create(
            player_name=player_name,
            phone_number=phone_number,
            partner_name=partner_name,
            player_email=player_email,
            partner_phone_number=partner_phone_number,
            partner_email=partner_email,
            partner_2_name = partner_2_name,
            partner_2_number = partner_2_number,
            partner_2_email = partner_2_email,
            category=category,
            payment_status='Pending'  # Add this field in model
        )

        # Redirect to payment page passing registration id
        return redirect('paymentgateway:payment_qr', registration_id=registration.id)

    return render(request, "registration.html")
    
def home(request):
    return render(request, "home.html")

def return_policies(request):
    return render(request, 'policies.html')