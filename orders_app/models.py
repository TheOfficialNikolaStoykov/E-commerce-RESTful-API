from django.db import models

from products_app.models import Product
from users_app.models import User


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
    ("pending", "Pending"),
    ("processing", "Processing"),
    ("shipping", "Shipping"),
    ("delivered", "Delivered"),
    ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, models.CASCADE)
    total_price = models.PositiveIntegerField()
    status = models.CharField(max_length=12, choices=ORDER_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=4, decimal_places=2)
    
class ShippingAddress(models.Model):
    order = models.ForeignKey(Order, models.CASCADE)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    postal_code = models.PositiveSmallIntegerField()
    country = models.CharField(max_length=10)