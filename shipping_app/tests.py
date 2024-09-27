from unittest.mock import MagicMock, patch

import shippo
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from cart_app.models import *
from orders_app.models import *
from payments_app.models import Payment
from products_app.models import *
from shipping_app.models import *
from users_app.models import User


class GetShippingRatesTestCase(APITestCase):
    """
    Test case for getting shipping rates.
    """

    def setUp(self):
        """
        Set up test data including users, orders, and shipping address.
        """
        self.admin_user = User.objects.create_superuser(username="test_admin_user", password="password")
        self.user = User.objects.create_user(username="test_user", password="password", first_name="Test")
        self.order_user = Order.objects.create(
                                            user=self.user,
                                            total_price=12.99,
                                            status="pending")
        
        self.valid_data = {
            "name": "John Doe",
            "street1": "123 Main St",
            "city": "Miami",
            "state": "FL",
            "zip": "33101",
            "country": "US"
        }

    @patch("shipping_app.calculate_shipping_rates.delivery_shippo.create_shipment")
    def test_get_shipping_rates_valid_request(self, mock_create_shipment):
        """
        Test getting shipping rates with valid request data.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        mock_create_shipment.return_value.rates = [
            shippo.models.components.Rate(
                provider="USPS", 
                servicelevel={"name": "Priority"}, 
                amount="10.00", 
                currency="USD", 
                estimated_days=3, 
                object_id="rate_123"
            )
        ]
        
        response = self.client.post(reverse("get-shipping-rates", args=(self.order_user.id,)), self.valid_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("provider", response.data[0])
        self.assertEqual(response.data[0]["provider"], "USPS")

    def test_get_shipping_rates_missing_fields(self):
        """
        Test getting shipping rates with missing address fields.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        invalid_data = self.valid_data.copy()
        invalid_data.pop("city")

        response = self.client.post(reverse("get-shipping-rates", args=(self.order_user.id,)), invalid_data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "All address fields are required")

    def test_get_shipping_rates_invalid_order(self):
        """
        Test getting shipping rates for an invalid order ID.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        invalid_order_id = 99999
        
        response = self.client.post(reverse("get-shipping-rates", args=(invalid_order_id,)), self.valid_data)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch("shipping_app.calculate_shipping_rates.delivery_shippo.create_shipment")
    def test_get_shipping_rates_shippo_error(self, mock_create_shipment):
        """
        Test handling a Shippo API error when getting shipping rates.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        mock_create_shipment.side_effect = Exception("Shippo API error")
        
        response = self.client.post(reverse("get-shipping-rates", args=(self.order_user.id,)), self.valid_data)
        
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Failed to get shipping rates: Shippo API error")

    def test_get_shipping_rates_unauthenticated(self):
        """
        Test getting shipping rates as an unauthenticated user.
        """
        response = self.client.post(reverse("get-shipping-rates", args=(self.order_user.id,)), self.valid_data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch("shipping_app.calculate_shipping_rates.delivery_shippo.create_shipment")
    def test_get_shipping_rates_valid_request(self, mock_create_shipment):
        """
        Test getting shipping rates with valid request and mocked Shippo rates.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        mock_rate = MagicMock()
        mock_rate.provider = "USPS"
        mock_rate.servicelevel.name = "Priority"
        mock_rate.amount = "10.00"
        mock_rate.currency = "USD"
        mock_rate.estimated_days = 3
        mock_rate.object_id = "rate_123"

        mock_create_shipment.return_value.rates = [mock_rate]

        response = self.client.post(reverse("get-shipping-rates", args=(self.order_user.id,)), self.valid_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("provider", response.data[0])
        self.assertEqual(response.data[0]["provider"], "USPS")
    
    def test_missing_required_address_fields(self):
        """
        Test getting shipping rates with missing required address fields.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        invalid_data = {
            "name": "John Doe",
            "street1": "123 Main St",
            "city": "Miami",
        }

        response = self.client.post(reverse("get-shipping-rates", args=(self.order_user.id,)), invalid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "All address fields are required")


class ShippingTestCase(APITestCase):
    """
    Test case for shipping-related endpoints.
    """

    def setUp(self):
        """
        Set up test data including users, orders, shipping addresses, products, and deliveries.
        """
        self.admin_user = User.objects.create_superuser(username="test_admin_user", password="password")
        self.user = User.objects.create_user(username="test_user", password="password", first_name="Test")
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
        self.shipping_address_user = ShippingAddress.objects.create(
            order=self.order_user,
            address_line_1="1101 Brickell Ave",
            address_line_2="Suite 800",
            city="Miami",
            state="FL",
            postal_code=33131,
            country="United States"
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
        self.shipping_method = ShippingMethod.objects.create(
            name="shippo",
            price=12.99)
        self.delivery = Delivery.objects.create(
            order=self.order_user,
            shipping_method=self.shipping_method,
            status="pending")
    
    def test_get_shipping_rates(self):
        """
        Test retrieving shipping rates.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        data = {
            "name": self.shipping_address_user.order.user.first_name,
            "street1": self.shipping_address_user.address_line_1,
            "city": self.shipping_address_user.city,
            "state": self.shipping_address_user.state,
            "zip": self.shipping_address_user.postal_code,
            "country": self.shipping_address_user.country,
        }

        response_shipping_rates = self.client.post(reverse("get-shipping-rates", args=(self.order_user.id,)), data)

        self.assertEqual(response_shipping_rates.status_code, status.HTTP_200_OK)
    
    def test_schedule_delivery(self):
        """
        Test scheduling a delivery with selected shipping rate.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        
        data = {
            "name": self.shipping_address_user.order.user.first_name,
            "street1": self.shipping_address_user.address_line_1,
            "city": self.shipping_address_user.city,
            "state": self.shipping_address_user.state,
            "zip": self.shipping_address_user.postal_code,
            "country": self.shipping_address_user.country,
        }

        response_shipping_rates = self.client.post(reverse("get-shipping-rates", args=(self.order_user.id,)), data)

        shipping_rates = response_shipping_rates.json()
        
        selected_rate = shipping_rates[0]["rate_id"]

        schedule_data = {
            "rate_id": selected_rate,
            "name": self.order_user.user.first_name,
            "street1": self.shipping_address_user.address_line_1,
            "city": self.shipping_address_user.city,
            "state": self.shipping_address_user.state,
            "zip": self.shipping_address_user.postal_code,
            "country": self.shipping_address_user.country,
        }

        response_schedule_delivery = self.client.post(reverse("schedule-delivery", args=(self.order_user.id,)), schedule_data)

        self.assertEqual(response_schedule_delivery.status_code, status.HTTP_201_CREATED)

    def test_change_delivery_status(self):
        """
        Test changing the status of a delivery.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        delivery = Delivery.objects.create(
            order=self.order_user,
            shipping_method=ShippingMethod.objects.create(name="USPS", price=10.0),
            tracking_number="123456789",
            shipping_label_url="http://example.com/label",
            status="pending"
        )

        data = {
            "status": "in_transit"
        }

        response = self.client.post(reverse("change-delivery-status", args=(delivery.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_check_delivery_status(self):
        """
        Test checking the status of a delivery.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        delivery = Delivery.objects.create(
            order=self.order_user,
            shipping_method=ShippingMethod.objects.create(name="USPS", price=10.0),
            tracking_number="123456789",
            shipping_label_url="http://example.com/label",
            status="pending"
        )

        response = self.client.get(reverse("check-delivery-status", args=(delivery.id,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_invalid_delivery_status(self):
        """
        Test updating delivery with an invalid status.
        """
        self.client.login(username=self.admin_user.username, password="password")
        self.token_admin = Token.objects.get(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {"status": "invalid_status"}

        response = self.client.post(reverse("change-delivery-status", args=(self.delivery.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid status")
    
    def test_no_rate_selected(self):
        """
        Test scheduling a delivery without selecting a rate.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        data = {}

        response = self.client.post(reverse("schedule-delivery", args=(self.order_user.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "No rate selected")

    @patch("shipping_app.calculate_shipping_rates.delivery_shippo.create_transaction")
    def test_failed_label_purchase_transaction_error(self, mock_create_transaction):
        """
        Test failed label purchase due to transaction error.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        mock_transaction = MagicMock()
        mock_transaction.status = shippo.models.components.TransactionStatusEnum.ERROR
        mock_transaction.messages = "Transaction failed"
        mock_create_transaction.return_value = mock_transaction

        data = {"rate_id": "rate_123"}

        response = self.client.post(reverse("schedule-delivery", args=(self.order_user.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Failed to purchase label: Transaction failed")

    @patch("shipping_app.calculate_shipping_rates.delivery_shippo.create_transaction")
    def test_failed_label_purchase_exception(self, mock_create_transaction):
        """
        Test failed label purchase due to an exception.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        mock_create_transaction.side_effect = Exception("Shippo API error")

        data = {"rate_id": "rate_123"}

        response = self.client.post(reverse("schedule-delivery", args=(self.order_user.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["error"], "Failed to purchase label: Shippo API error")