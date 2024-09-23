from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import OpenApiResponse, extend_schema

from cart_app.models import *
from .serializers import *


@extend_schema(
    responses={200: OrderViewSerializer(many=True)},
    description="List all orders. Accessible only to admin users."
)
@api_view(["GET"])
@permission_classes([IsAdminUser])
def list_orders_view(request):
    """
    List all orders. Accessible only to admin users.
    """
    orders = Order.objects.all()
    
    serializer = OrderViewSerializer(orders, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    responses={200: OrderViewSerializer(many=True)},
    description="List the authenticated user's orders."
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def view_orders_view(request):
    """
    List the authenticated user's orders.
    """
    user = request.user
    
    orders = Order.objects.filter(user=user)
    
    serializer = OrderViewSerializer(orders, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    responses={200: OrderViewSerializer},
    description="Retrieve a single order by its ID. Accessible only to admin users."
)
@api_view(["GET"])
@permission_classes([IsAdminUser])
def retrieve_single_order_view_admin(request, pk):
    """
    Retrieve a single order by its ID. Accessible only to admin users.
    """
    order = get_object_or_404(Order, pk=pk)
    
    serializer = OrderViewSerializer(order)
    return Response(serializer.data)


@extend_schema(
    responses={200: OrderViewSerializer},
    description="Retrieve a single order for the authenticated user by its ID."
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrieve_single_order_view_user(request, pk):
    """
    Retrieve a single order for the authenticated user by its ID.
    """
    user = request.user
    order = get_object_or_404(Order, user=user, pk=pk)
    
    serializer = OrderViewSerializer(order)
    return Response(serializer.data)


@extend_schema(
    request=OrderCreateSerializer,
    responses={
        201: OrderCreateSerializer,
        400: OpenApiResponse(description="Bad Request")
    },
    description="Checkout the authenticated user's cart and create an order."
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def checkout_cart_view(request, pk):
    """
    Checkout the authenticated user's cart and create an order.
    """
    user = request.user
    cart = get_object_or_404(Cart, pk=pk, user=user)
    serializer = OrderCreateSerializer(data=request.data, context={"request": request})

    if serializer.is_valid():
        order = serializer.save()
        response_serializer = OrderCreateSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=OrderCreateSerializer,
    responses={
        200: OrderCreateSerializer,
        400: OpenApiResponse(description="Bad Request")
    },
    description="Change the status of an order. Accessible only to admin users."
)
@api_view(["PATCH"])
@permission_classes([IsAdminUser])
def change_order_status_view(request, pk):
    """
    Change the status of an order. Accessible only to admin users.
    """
    order = get_object_or_404(Order, pk=pk)
    serializer = OrderCreateSerializer(order, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
