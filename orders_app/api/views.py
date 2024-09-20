from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from cart_app.models import *

from .serializers import *


@api_view(["GET"])
@permission_classes([IsAdminUser])
def list_orders_view(request):
    orders = Order.objects.all()
    
    serializer = OrderViewSerializer(orders, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def view_orders_view(request):
    user = request.user
    
    orders = Order.objects.filter(user=user)
    
    serializer = OrderViewSerializer(orders, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAdminUser])
def retrieve_single_order_view_admin(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    serializer = OrderViewSerializer(order)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrieve_single_order_view_user(request, pk):
    user = request.user
    order = get_object_or_404(Order, user=user, pk=pk)
    
    serializer = OrderViewSerializer(order)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def checkout_cart_view(request, pk):
    user = request.user
    cart = get_object_or_404(Cart, pk=pk, user=user)
    serializer = OrderCreateSerializer(data=request.data, context={"request": request})

    if serializer.is_valid():
        order = serializer.save()
        response_serializer = OrderCreateSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PATCH"])
@permission_classes([IsAdminUser])
def change_order_status_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    serializer = OrderCreateSerializer(order, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    