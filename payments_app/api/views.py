from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from orders_app.models import Order
from payments_app.models import Payment, Transaction
from payments_app.process_payment import process_payment_stripe

from .permissions import IsOwnerOrAdmin
from .serializers import PaymentSerializer


@extend_schema(
    request=None,
    responses={
        201: OpenApiResponse(description="Payment processed successfully"),
        400: OpenApiResponse(description="Bad Request")
    },
    description="Process payment for an order."
)
@api_view(["POST"])
def process_payment(request, id):
    """
    Process payment for an order.
    """
    order = get_object_or_404(Order, id=id, user=request.user)
    if order.status != "pending":
        return Response({"error": "Order is not eligible for payment."}, status=status.HTTP_400_BAD_REQUEST)
    
    payment_method = request.data.get("payment_method")
    
    if not payment_method:
        return Response({"error": "Payment method is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    amount = order.total_price
    
    payment_result = process_payment_stripe(amount, payment_method)
    
    payment = Payment.objects.create(
        order=order,
        amount=amount,
        status=payment_result["status"],
        payment_method=payment_method
    )
    
    Transaction.objects.create(
        payment=payment,
        status=payment_result["status"]
    )
    
    if payment.status == "completed":
        order.status = "completed"
        order.save()

    return Response({"message": "Payment processed successfully", "status": payment.status}, status=status.HTTP_201_CREATED)


@extend_schema(
    responses={200: PaymentSerializer},
    description="Retrieve payment status for a specific payment."
)
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsOwnerOrAdmin])
def get_payment_status(request, id):
    """
    Retrieve payment status for a specific payment.
    """
    payment = get_object_or_404(Payment, id=id)
    
    serializer = PaymentSerializer(payment)
    
    return Response(serializer.data)