from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from cart_app.models import *
from orders_app.models import *
from payments_app.models import Payment
from payments_app.process_payment import *
from products_app.models import *
from users_app.models import User


class PaymentTestCase(APITestCase):
    """
    Test case for payment-related endpoints.
    """

    def setUp(self):
        """
        Set up test data, including users, orders, cart, and payment.
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
        self.payment = Payment.objects.create(
            order=self.order_user,
            amount=self.order_user.total_price,
            status="pending",
            payment_method="stripe"
        )

    def test_process_payment(self):
        """
        Test processing a payment for an order.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        data = {
            "payment_platform": "stripe"
        }

        response = self.client.post(reverse("process-payment", args=(self.order_user.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_process_payment_invalid_status(self):
        """
        Test processing a payment with an invalid order status.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        order = Order.objects.create(
            user=self.user,
            total_price=12.99,
            status="invalid_status"
        )

        response = self.client.post(reverse("process-payment", args=(order.id,)))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_process_payment_no_payment_method(self):
        """
        Test processing a payment with no payment method provided.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.post(reverse("process-payment", args=(self.order_user.id,)), {"payment_platform": ""})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_process_payment_invalid_payment_method(self):
        """
        Test processing a payment with an invalid payment method.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        data = {
            "payment_platform": "invalid_payment_method"
        }

        response = self.client.post(reverse("process-payment", args=(self.order_user.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_payment_status(self):
        """
        Test retrieving the status of a payment.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.get(reverse("get-payment-status", args=(self.payment.id,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class IsOwnerOrAdminPermissionTestCase(APITestCase):
    """
    Test case for testing permissions for owners and admins.
    """

    def setUp(self):
        """
        Set up test data, including users, orders, cart, and payment.
        """
        self.admin_user = User.objects.create_superuser(username="test_user_admin", password="password")
        self.user_owner = User.objects.create_user(username="owner", password="password")
        self.other_user = User.objects.create_user(username="other_user", password="password")

        self.brand = Brand.objects.create(
            name="Test Brand",
            description="Test Brand Description"
        )
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Category Description"
        )
        self.product = Product.objects.create(
            name="Test Product", description="Test Product Description", price=50, stock=20,
            category=self.category, brand=self.brand
        )
        self.order_owner = Order.objects.create(user=self.user_owner, total_price=50, status="pending")
        self.cart = Cart.objects.create(user=self.user_owner)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        self.payment = Payment.objects.create(order=self.order_owner, amount=50, status="pending", payment_method="stripe")

    def test_admin_access(self):
        """
        Test that an admin can access payment status.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.get(reverse("get-payment-status", args=(self.payment.id,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_access(self):
        """
        Test that the owner can access their payment status.
        """
        self.client.login(username=self.user_owner.username, password=self.user_owner.password)
        self.token_owner = Token.objects.get(user__username=self.user_owner.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_owner.key)

        response = self.client.get(reverse("get-payment-status", args=(self.payment.id,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_owner_no_access(self):
        """
        Test that a non-owner cannot access payment status.
        """
        self.client.login(username=self.other_user.username, password=self.other_user.password)
        self.token_other_user = Token.objects.get(user__username="other_user")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_other_user.key)

        response = self.client.get(reverse("get-payment-status", args=(self.payment.id,)))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProcessPaymentStripeTestCase(APITestCase):
    """
    Test case for processing payments using Stripe.
    """

    @patch("payments_app.process_payment.stripe.PaymentIntent.create")
    def test_process_payment_stripe_success(self, mock_create):
        """
        Test successful Stripe payment.
        """
        mock_create.return_value = {
            "id": "pi_123456789",
            "status": "succeeded"
        }

        result = process_payment_stripe(amount=100, payment_method=["card"])

        self.assertEqual(result["transaction_id"], "pi_123456789")
        self.assertEqual(result["status"], "completed")

    @patch("payments_app.process_payment.stripe.PaymentIntent.create")
    def test_process_payment_stripe_failure(self, mock_create):
        """
        Test failed Stripe payment (StripeError).
        """
        mock_create.side_effect = stripe.error.StripeError("Payment failed")

        result = process_payment_stripe(amount=100, payment_method=["card"])

        self.assertEqual(result["status"], "failed")