from django.db import models

from orders_app.models import Order


class ShippingMethod(models.Model):
    SHIPPING_METHOD_CHOICES = [
    ("shippo", "Shippo"),
    ]
    name = models.CharField(max_length=6, choices=SHIPPING_METHOD_CHOICES)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    
class Delivery(models.Model):
    SHIPPING_STATUS_CHOICES = [
    ("pending", "Pending"),
    ("in_transit", "In transit"),
    ("out_for_delivery", "Out for delivery"),
    ("delivered", "Delivered"),
    ("failed", "Failed"),
    ]
    
    order = models.ForeignKey(Order, models.CASCADE)
    shipping_method = models.OneToOneField(ShippingMethod, on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=30)
    shipping_label_url = models.URLField()
    status=models.CharField(max_length=16, choices=SHIPPING_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)