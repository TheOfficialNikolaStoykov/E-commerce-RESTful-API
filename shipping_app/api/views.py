import shippo
import shippo.models
import shippo.models.components
import shippo.models.errors
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from orders_app.models import Order
from shipping_app.calculate_shipping_rates import delivery_shippo

from .serializers import *


@extend_schema(
    request=None,
    responses={200: OpenApiResponse(response=None, description="List of shipping rates")},
    description="Get shipping rates for an order."
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def get_shipping_rates(request, id):
    """
    Get shipping rates for an order.
    """
    order = get_object_or_404(Order, id=id, user=request.user)

    name = request.data.get("name")
    street1 = request.data.get("street1")
    city = request.data.get("city")
    state = request.data.get("state")
    zip = request.data.get("zip")
    country = request.data.get("country")

    if not all([name, street1, city, state, zip, country]):
        return Response({"error": "All address fields are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    shipping_method = ShippingMethod.objects.create(
        name="shippo",
        price=order.total_price
    )
    
    delivery_shippo.name = name
    delivery_shippo.street1 = street1
    delivery_shippo.city = city
    delivery_shippo.state = state
    delivery_shippo.zip = zip
    delivery_shippo.country = country
    delivery_shippo.create_address_from()
    delivery_shippo.create_address_to()
    delivery_shippo.create_parcel()

    try:
        shipment = delivery_shippo.create_shipment()
    except Exception as e:
        return Response({"error": f"Failed to get shipping rates: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    rates = []
    for rate in shipment.rates:
        rates.append({
            "provider": rate.provider,
            "servicelevel": rate.servicelevel.name,
            "amount": rate.amount,
            "currency": rate.currency,
            "estimated_days": rate.estimated_days,
            "rate_id": rate.object_id
        })
    
    return Response(rates, status=status.HTTP_200_OK)


@extend_schema(
    request=None,
    responses={201: OpenApiResponse(response=None, description="Label purchased successfully")},
    description="Schedule a delivery for an order using a selected shipping rate."
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def schedule_delivery(request, id):
    """
    Schedule a delivery for an order using a selected shipping rate.
    """
    order = get_object_or_404(Order, id=id, user=request.user)

    selected_rate_id = request.data.get("rate_id")
    if not selected_rate_id:
        return Response({"error": "No rate selected"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        delivery_shippo.rate_id = selected_rate_id
        transaction = delivery_shippo.create_transaction()
    except Exception as e:
        return Response({"error": f"Failed to purchase label: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if transaction.status != shippo.models.components.TransactionStatusEnum.SUCCESS:
        return Response({"error": f"Failed to purchase label: {transaction.messages}"}, status=status.HTTP_400_BAD_REQUEST)

    shipping_method = ShippingMethod.objects.create(
        name="shippo",
        price=order.total_price
    )

    delivery = Delivery.objects.create(
        order=order,
        shipping_method=shipping_method,
        tracking_number=transaction.tracking_number,
        shipping_label_url=transaction.label_url,
        status="pending"
    )

    return Response({
        "message": "Label purchased successfully",
        "tracking_number": delivery.tracking_number,
        "label_url": delivery.shipping_label_url,
        "tracking_url": transaction.tracking_url_provider,
        "status": delivery.status
    }, status=status.HTTP_201_CREATED)


@extend_schema(
    request=None,
    responses={200: OpenApiResponse(response=None, description="Delivery status updated successfully")},
    description="Change the delivery status for an order."
)
@api_view(["POST"])
@permission_classes([IsAdminUser])
def change_delivery_status(request, id):
    """
    Change the delivery status for an order.
    """
    delivery = get_object_or_404(Delivery, id=id)
    
    new_status = request.data.get("status")
    
    if new_status not in dict(Delivery.SHIPPING_STATUS_CHOICES):
        return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
    
    delivery.status = new_status
    delivery.save()
    
    return Response({
        "message": "Delivery status updated successfully",
        "new_status": delivery.status
    }, status=status.HTTP_200_OK)


@extend_schema(
    responses={200: DeliverySerializer},
    description="Check the delivery status of an order."
)
@api_view(["GET"])
@permission_classes([IsAdminUser])
def check_delivery_status(request, id):
    """
    Check the delivery status of an order.
    """
    delivery = get_object_or_404(Delivery, id=id)
    
    serializer = DeliverySerializer(delivery)
    
    return Response(serializer.data)
