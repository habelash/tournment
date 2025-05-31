from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from registration.models import TournamentRegistration, Payment
# from paytmchecksum import PaytmChecksum
from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


import hashlib
import hmac
import base64
import random
import time
import json


def generate_checksum(params: dict, merchant_key: str) -> str:
    params_string = create_param_string(params)
    digest = hmac.new(merchant_key.encode(), params_string.encode(), hashlib.sha256).digest()
    checksum = base64.b64encode(digest).decode()
    return checksum

def verify_checksum(params: dict, merchant_key: str, checksum: str) -> bool:
    params = {k: v for k, v in params.items() if k != "CHECKSUMHASH"}
    generated_checksum = generate_checksum(params, merchant_key)
    return generated_checksum == checksum

def create_param_string(params: dict) -> str:
    keys = sorted(params.keys())
    param_str = '|'.join(str(params[key]) for key in keys if params[key] is not None)
    return param_str



MERCHANT_ID = "DIY12386817555501617"
MERCHANT_KEY = "bKMfNxPPf_QdZppa"
WEBSITE = "WEBSTAGING"
INDUSTRY_TYPE_ID = "Retail"
CHANNEL_ID = "WEB"
CALLBACK_URL = "http://127.0.0.1:8000/paytm/response/"
# CALLBACK_URL = "https://securegw-stage.paytm.in/theia/paytmCallback"

def initiate_payment(request, registration_id):
    import uuid
    order_id = "ORDER_" + str(int(time.time())) + str(random.randint(1000, 9999))

    registration = get_object_or_404(TournamentRegistration, id=registration_id)

    amount = "1"  # For example
    customer_id = registration.phone_number

    paytmParams = {
        "MID": MERCHANT_ID,
        "ORDER_ID": order_id,
        "CUST_ID": customer_id,
        "TXN_AMOUNT": amount,
        "CHANNEL_ID": CHANNEL_ID,
        "WEBSITE": WEBSITE,
        "INDUSTRY_TYPE_ID": INDUSTRY_TYPE_ID,
        "CALLBACK_URL": CALLBACK_URL,
    }
    # checksum = PaytmChecksum.generateSignature(paytmParams, MERCHANT_KEY)
    checksum = generate_checksum(paytmParams, MERCHANT_KEY)
    paytmParams["CHECKSUMHASH"] = checksum
    
    return render(request, "paytm_redirect.html", {"registration": registration, "paytm_params": paytmParams})

def send_transaction_email(player_email, partner_email, partner_2_email, player_name, partner_name, partner_2_name, category, paytm_params):
    subject = "Shuttle Up - Tournament Registration Confirmation"

    # Create greeting based on category, no trailing commas
    if category.lower() == "singles":
        greeting = f"{player_name}"
        recipients = [player_email]
    elif category.lower() == "triplets":
        greeting = f"{player_name}, {partner_name}, and {partner_2_name}"
        recipients = [email for email in [player_email, partner_email, partner_2_email] if email]
    else:  # Doubles or Mixed Doubles
        greeting = f"{player_name} and {partner_name}"
        recipients = [email for email in [player_email, partner_email] if email]

    # Build the message
    from_email = "StringsAttched@gmail.com"
    to_email = recipients

    html_content = render_to_string('confirmation_email.html', {
        'greeting': greeting,
        'category': category,
        'paytm_params': paytm_params,
    })

    msg = EmailMultiAlternatives(subject, "", from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@csrf_exempt
def payment_response(request,registration_id):
    # received_data = dict(request.POST)
    # paytm_checksum = received_data.get("CHECKSUMHASH", "")
    
    # # Verify checksum with your checksum function here
    # is_valid_checksum = verify_checksum(received_data, MERCHANT_KEY, paytm_checksum)
    
    # order_id = received_data.get("ORDER_ID")
    
    # # Parse registration id from order_id or store order_id in model in Step 1
    # registration_id = int(order_id.split("_")[-1])  # example parsing if order_id = 'ORDER_123'
    # registration = get_object_or_404(TournamentRegistration, id=registration_id)

    # # Save payment details (assuming you have Payment model linked)
    # Payment.objects.create(
    #     registration=registration,
    #     order_id=order_id,
    #     txn_id=received_data.get("TXNID", ""),
    #     txn_amount=received_data.get("TXNAMOUNT", ""),
    #     status=received_data.get("STATUS", ""),
    #     response_data=json.dumps(received_data),
    # )

    # # Update registration payment status
    # if received_data.get("STATUS") == "TXN_SUCCESS":
    #     registration.payment_status = "Success"
    # else:
    #     registration.payment_status = "Failed"
    # registration.save()

    # # Show confirmation page with payment status
    # return render(request, "payment_response.html", {
    #     "data": received_data,
    #     "checksum_valid": is_valid_checksum,
    #     "registration": registration,
    # })


    # Simulate Paytm POST data (normally comes from Paytm)
    paytm_params = {
        "ORDERID": registration_id,
        "TXNID": "TEST_TXN_001",
        "TXNAMOUNT": request.POST.get("TXNAMOUNT", "1.00"),
        "STATUS": "TXN_SUCCESS"
    }

    order_id = registration_id

    # Lookup your saved registration (you can parse ORDERID if needed)
    registration = TournamentRegistration.objects.filter(id=order_id).first()

    if registration:
        # Save the payment details
        Payment.objects.create(
            registration=registration,
            order_id=paytm_params["ORDERID"],
            txn_id=paytm_params["TXNID"],
            txn_amount=paytm_params["TXNAMOUNT"],
            status="TXN_SUCCESS",
            response_data=json.dumps(paytm_params),
        )

        # Update registration payment status
        registration.payment_status = "Paid"
        registration.save()

        # Get player info from your model or request
        player_name = registration.player_name 
        partner_name = registration.partner_name 
        player_email = registration.player_email
        partner_email = registration.partner_email
        partner_2_email = registration.partner_2_email
        player_name = registration.player_name
        partner_name = registration.partner_name
        partner_2_name = registration.partner_2_name
        category = registration.category

        send_transaction_email(player_email, partner_email, partner_2_email, player_name, partner_name, partner_2_name, category, paytm_params)
        


    context = {
        "data": paytm_params,
        "checksum_is_valid": True,  # Simulate checksum verification success
    }

    return render(request, "paytm_response.html", context)