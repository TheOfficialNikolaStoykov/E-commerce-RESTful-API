from django.db import models

from products_app.models import Product
from users_app.models import User


class Cart(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)