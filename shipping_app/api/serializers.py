from rest_framework import serializers

from shipping_app.models import *


class ShippingMethodSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ShippingMethod
        fields = "__all__"

class DeliverySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Delivery
        fields = "__all__"