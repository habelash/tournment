from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    receipt = models.FileField(upload_to='receipts/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"