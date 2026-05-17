from django.db import models
from django.contrib.auth.models import User

class PaymentRecord(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.TextField()  # This will store encrypted text
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)