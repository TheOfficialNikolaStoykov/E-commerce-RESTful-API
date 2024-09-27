from rest_framework import serializers

from cart_app.models import CartItem
from orders_app.models import *


class OrderCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = fields = ["id", "created_at", "updated_at", "status"]
    
    def create(self, validated_data):
        user = self.context["request"].user
        
        cart_items = CartItem.objects.filter(cart__user=user)
        
        if not cart_items.exists():
            raise serializers.ValidationError("Your cart is empty.")
        
        total_price = 0
        for cart_item in cart_items:
            total_price += cart_item.product.price * cart_item.quantity
        
        order = Order.objects.create(
            user=user,
            total_price= total_price,
            status="pending"
            )
        
        for cart_item in cart_items:
            OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price
            )
        
        cart_items.delete()
        
        return order

class OrderViewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderItem
        fields = "__all__"

class ShippingAddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ShippingAddress
        fields = "__all__"