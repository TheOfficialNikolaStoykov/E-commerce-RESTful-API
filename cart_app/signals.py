from django.db.models.signals import post_save
from django.dispatch import receiver

from cart_app.models import Cart
from orders_app.models import Order, OrderItem


@receiver(post_save, sender=Cart)
def create_order(sender, instance, created, **kwargs):
    
    if created:
        
        for cart_item in instance.cart_items.all():
            total_price += cart_item.product.price * cart_item.quantity
        
            order = Order.objects.create(
            user=instance.user,
            total_price= total_price,
            status="pending"
            )
         
            OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price
            )