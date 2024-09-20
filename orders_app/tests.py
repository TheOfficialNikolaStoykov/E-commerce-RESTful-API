from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from cart_app.models import *
from products_app.models import *

from .models import *


class OrderTestCase(APITestCase):
    
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username="test_admin_user", password="password")
        self.user = User.objects.create_user(username="test_user", password="password")
        self.order_admin = Order.objects.create(
            user=self.admin_user,
            total_price=12.99,
            status="pending"
        )
        self.order_user = Order.objects.create(
            user=self.user,
            total_price=12.99,
            status="pending"
        )
        self.brand = Brand.objects.create(
            name="Test Brand",
            description="Test Description"
        )
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description"
        )
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Descripion",
            price=99.99,
            stock=10,
            category=self.category,
            brand=self.brand
            )
        self.cart = Cart.objects.create(
            user=self.user
        )
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product
        )
        
    def test_list_orders(self):
        self.client.login(username="test_admin_user", password="password")
        self.token_admin = Token.objects.get(user__username=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)
        
        response = self.client.get(reverse("orders"))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_view_orders_user(self):
        self.client.login(username="test_user", password="password")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        
        response = self.client.get(reverse("orders-view-user"))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_single_order_admin(self):
        self.client.login(username="test_admin_user", password="password")
        self.token_admin = Token.objects.get(user__username=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)
        
        response = self.client.get(reverse("order-single-admin", args=(self.order_admin.id,)))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_retrieve_single_order_user(self):
        self.client.login(username="test_user", password="password")
        self.token_admin = Token.objects.get(user__username=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)
        
        response = self.client.get(reverse("order-single-admin", args=(self.order_user.id,)))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_checkout_cart(self):
        self.client.login(username="test_user", password="password")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.post(reverse("cart-checkout", args=(self.cart.id,)))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_change_order_status(self):
        self.client.login(username="test_admin_user", password="password")
        self.token = Token.objects.get(user__username=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        
        data = {
            "status": "processing"
        }

        response = self.client.patch(reverse("order-change-status", args=(self.order_admin.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)