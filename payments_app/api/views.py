from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

    request_payment_platform = request.data.get("payment_platform")

    payment_platform_choices = []
    
    for payment_platform in Payment.PAYMENT_PLATFORM_CHOICES:
        payment_platform_choices.append(payment_platform[0])
    
    if not request_payment_platform:
        return Response({"error": "Payment method is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    if request_payment_platform not in payment_platform_choices:
        return Response({"error": "Invalid payment method."}, status=status.HTTP_400_BAD_REQUEST)
    
    amount = order.total_price
    
    payment_result = process_payment_stripe(amount, request_payment_platform)
    
    payment = Payment.objects.create(
        order=order,
        amount=amount,
        status=payment_result["status"],
        payment_method=payment_platform
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
class PaymentDetailView(RetrieveAPIView):
    """Retrieve payment status for a specific payment."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]