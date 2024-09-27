from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart_app.models import *

from .serializers import *


@extend_schema(
    responses={200: CartSerializer},
    description="Retrieve the authenticated user's cart details."
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def view_cart_view(request):
    """
    Retrieve the authenticated user's cart details.
    """
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user)

    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    request=CartItemSerializer,
    responses={200: CartSerializer},
    description="Add an item to the authenticated user's cart."
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_cart_item_view(request):
    """
    Add an item to the authenticated user's cart.
    """
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


@extend_schema(
    request=CartItemSerializer,
    responses={200: CartItemSerializer},
    description="Edit an item in the authenticated user's cart."
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def edit_cart_item_view(request, pk):
    """
    Edit an item in the authenticated user's cart.
    """
    cart_item = get_object_or_404(CartItem, pk=pk)
    
    serializer = CartItemSerializer(cart_item, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={200: None},
    description="Delete an item from the authenticated user's cart."
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_cart_item_view(request, pk):
    """
    Delete an item from the authenticated user's cart.
    """
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()
    return Response(status=status.HTTP_200_OK)


@extend_schema(
    responses={204: None},
    description="Clear all items from the authenticated user's cart."
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def clear_cart_items_view(request):
    """
    Clear all items from the authenticated user's cart.
    """
    user = request.user    
    cart, _ = Cart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_items.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
