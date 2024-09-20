from django.db import models

from orders_app.models import Order


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
    ("pending", "Pending"),
    ("completed", "Completed"),
    ("failed", "Failed")
    ]
    PAYMENT_PLATFORM_CHOICES = [
    ("stripe", "Stripe")
    ]
    order = models.ForeignKey(Order, models.CASCADE)
    amount = models.DecimalField(max_digits=4, decimal_places=2)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES)
    payment_method = models.CharField(max_length=11, choices=PAYMENT_PLATFORM_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

class Transaction(models.Model):
    TRANSACTION_STATUS_CHOICES = [
    ("success", "Success"),
    ("failed", "Failed")
    ]
    payment = models.ForeignKey(Payment, models.CASCADE)
    status = models.CharField(max_length=10, choices=TRANSACTION_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

