from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from cart_app.models import *
from orders_app.api.serializers import OrderCreateSerializer
from products_app.models import *

from .models import *


class OrderTestCase(APITestCase):
    """
    Test case for order-related endpoints.
    """

    def setUp(self):
        """
        Set up test data including users, orders, cart, and products.
        """
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
            description="Test Description",
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
        """
        Test listing all orders as an admin.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.get(reverse("orders"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_orders_user(self):
        """
        Test listing orders of a specific user.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.get(reverse("orders-view-user"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_single_order_admin(self):
        """
        Test retrieving a single order as an admin.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.get(reverse("order-single-admin", args=(self.order_admin.id,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_single_order_user(self):
        """
        Test retrieving a single order as a user.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.get(reverse("order-single-user", args=(self.order_user.id,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_checkout_cart_empty_cart(self):
        """
        Test attempting to checkout with an empty cart.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        CartItem.objects.filter(cart=self.cart).delete()

        data = {
            "status": "pending"
        }

        response = self.client.post(reverse("cart-checkout", args=(self.cart.id,)), data)

        self.assertIn("Your cart is empty.", str(response.data[0]))

    def test_checkout_cart_invalid_status(self):
        """
        Test attempting to checkout with an invalid status.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        data = {
            "status": "invalid_status"
        }

        response = self.client.post(reverse("cart-checkout", args=(self.cart.id,)), data)

        self.assertIn("is not a valid choice.", response.data["status"][0])

    def test_checkout_cart_201(self):
        """
        Test successfully checking out a cart.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        data = {
            "status": "pending"
        }

        response = self.client.post(reverse("cart-checkout", args=(self.cart.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_change_order_status_200(self):
        """
        Test changing the status of an order as an admin (valid data).
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {
            "status": "processing"
        }

        response = self.client.patch(reverse("order-change-status", args=(self.order_admin.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_order_status_400(self):
        """
        Test changing the status of an order with invalid data (expecting 400 Bad Request).
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {
            "status": "",
        }

        response = self.client.patch(reverse("order-change-status", args=(self.order_admin.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)