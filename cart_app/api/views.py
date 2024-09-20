from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from cart_app.models import *

from .serializers import *


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def view_cart_view(request):
    user = request.user

    cart, _ = Cart.objects.get_or_create(user=user)

    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_cart_item_view(request):
    user = request.user
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')
    
    product = get_object_or_404(Product, id=product_id)
        
    cart, _ = Cart.objects.get_or_create(user=user)
    
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        cart_item.quantity += int(quantity)
    else:
        cart_item.quantity = int(quantity)
        
    cart_item.save()
    
    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def edit_cart_item_view(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    
    serializer = CartItemSerializer(cart_item, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_cart_item_view(request, pk):       
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()
    return Response(status=status.HTTP_200_OK)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def clear_cart_items_view(request):
    user = request.user    
    cart, _ = Cart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_items.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)