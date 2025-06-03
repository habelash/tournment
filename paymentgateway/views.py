from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from registration.models import TournamentRegistration, Payment
import requests
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import JsonResponse
import razorpay
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

def send_transaction_email(player_email, partner_email, partner_2_email, player_name, partner_name, partner_2_name, category, paytm_params):
    subject = "Shuttle Up - Tournament Registration Confirmation"

    # Create greeting based on category, no trailing commas
    if category.lower() == "singles":
        greeting = f"{player_name}"
        recipients = [player_email]
    elif category.lower() == "triplets":
        greeting = f"{player_name}, {partner_name}, and {partner_2_name}"
        recipients = [email.strip() for email in [player_email, partner_email, partner_2_email] if email]
    else:  # Doubles or Mixed Doubles
        greeting = f"{player_name} and {partner_name}"
        recipients = [email.strip() for email in [player_email, partner_email] if email]

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


def initiate_payment(request,registration_id):

        # Lookup your saved registration (you can parse ORDERID if needed)
        registration = TournamentRegistration.objects.filter(id=registration_id).first()
        category = registration.category
        if category == 'singles':
            amount = 59900
        if category == 'triplets':
            amount = 99900
        else :
            amount == 79900
        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # Sample data – replace with actual user and amount
        order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1"
        })

         # ✅ Save the generated order ID
        registration.razorpay_order_id = order['id']
        registration.save()

        context = {
            'payment': order,
            'razorpay_order_id': order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount': amount
        }

        return render(request, 'payment_redirect.html', context)


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.POST
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            })

            registration = TournamentRegistration.objects.get(razorpay_order_id=data['razorpay_order_id'])
            category = registration.category
            if category == 'singles':
                amount = 59900
            if category == 'triplets':
                amount = 79900
            else :
                amount = 99900
            if registration:
        # Save the payment details
                Payment.objects.create(
                    registration=registration,
                    order_id=data['razorpay_order_id'],
                    txn_id=data['razorpay_payment_id'],
                    txn_amount=amount/100,
                    status="TXN_SUCCESS",
                    response_data=data,
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
                category = registration.get_category_display()

                    # Simulate Paytm POST data (normally comes from Paytm)
                payment_params = {
                    "ORDERID": data['razorpay_order_id'],
                    "TXNID": data['razorpay_payment_id'],
                    "TXNAMOUNT": amount/100,
                    "STATUS": "TXN_SUCCESS"
                }

                send_transaction_email(player_email, partner_email, partner_2_email, player_name, partner_name, partner_2_name, category, payment_params)
                

            # ✅ Payment is successful and verified
            return render(request, 'payment_success.html')
        except razorpay.errors.SignatureVerificationError:
            return render(request,'payment_failure.html')
        
    
    elif request.method == "GET":
        data = request.GET
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            # Safely extract data
            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_signature = data.get('razorpay_signature')

            # Verify signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })

            registration = TournamentRegistration.objects.get(razorpay_order_id=razorpay_order_id)
            category = registration.category

            # Determine amount
            if category == 'singles':
                amount = 100
            elif category == 'triplets':
                amount = 79900
            else:
                amount = 99900  # fixed: assignment not comparison

            # Save payment info
            Payment.objects.create(
                registration=registration,
                order_id=razorpay_order_id,
                txn_id=razorpay_payment_id,
                txn_amount=amount/100,
                status="TXN_SUCCESS",
                response_data=data,
            )

            # Update registration status
            registration.payment_status = "Paid"
            registration.save()

            # Extract email & name details
            player_name = registration.player_name
            partner_name = registration.partner_name
            partner_2_name = registration.partner_2_name
            player_email = registration.player_email
            partner_email = registration.partner_email
            partner_2_email = registration.partner_2_email
            category_display = registration.get_category_display()

            payment_params = {
                "ORDERID": razorpay_order_id,
                "TXNID": razorpay_payment_id,
                "TXNAMOUNT": amount/100,
                "STATUS": "TXN_SUCCESS"
            }

            send_transaction_email(
                player_email, partner_email, partner_2_email,
                player_name, partner_name, partner_2_name,
                category_display, payment_params
            )

            return render(request, 'payment_success.html')

        except razorpay.errors.SignatureVerificationError as e:
            return render(request, 'payment_failure.html')

    else:
        return render(request, 'payment_failed.html')