from django.db import models

# Create your models here.
CATEGORY_CHOICES = [
    ('singles', 'Singles'),
    ('beginner_doubles', 'Beginner Doubles'),
    ('intermediate_mens_doubles', 'Intermediate Mens Doubles'),
    ('intermediate_+_mens_doubles', 'Intermediate+ Mens Doubles'),
    ('advanced_mens_doubles', 'Advanced Mens Doubles'),
    ('womens_doubles', 'Womens Doubles'),
    ('mixed_doubles', 'Mixed Doubles'),
    ('triplets', 'Triplets'),
]

class TournamentRegistration(models.Model):
    player_name = models.CharField(max_length=100)
    partner_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Player's phone number
    partner_phone_number = models.CharField(max_length=15, blank=True, null=True)  # New field

    player_email = models.EmailField(blank=True, null=True)  # New field
    partner_email = models.EmailField(blank=True, null=True)  # New field

    partner_2_name = models.CharField(max_length=100, blank=True, null=True)
    partner_2_number = models.CharField(max_length=15, blank=True, null=True)  # Player's phone number
    partner_2_email = models.EmailField(blank=True, null=True)  # New field

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=20, default='Pending')  # Payment status

    def __str__(self):
        return f"{self.player_name} - {self.category}"


class Payment(models.Model):
    registration = models.ForeignKey(TournamentRegistration, on_delete=models.CASCADE, related_name='payments')
    order_id = models.CharField(max_length=100)
    txn_id = models.CharField(max_length=100, blank=True, null=True)
    txn_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    response_data = models.TextField()  # Store full response JSON/text
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.registration.player_name} - {self.order_id} - {self.status}"