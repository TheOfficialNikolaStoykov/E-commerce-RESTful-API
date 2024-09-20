from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from cart_app.models import *
from orders_app.models import *
from payments_app.models import Payment
from products_app.models import *
from users_app.models import User
from shipping_app.models import *


class UserTestCase(APITestCase):
    
    def setUp(self):
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
        self.payment = Payment.objects.create(
            order=self.order_user,
            amount=self.order_user.total_price,
            status="pending",
            payment_method="stripe"
        )
    
    def test_schedule_delivery(self):
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        data = {
            "name": self.order_user.user.first_name,
            "street1": self.shipping_address_user.address_line_1,
            "city": self.shipping_address_user.city,
            "state": self.shipping_address_user.state,
            "zip": self.shipping_address_user.postal_code,
            "country": self.shipping_address_user.country,
        }

        response_shipping_rates = self.client.post(reverse("get-shipping-rates", args=(self.order_user.id,)), data)

        self.assertEqual(response_shipping_rates.status_code, status.HTTP_200_OK)

        shipping_rates = response_shipping_rates.json()
        
        selected_rate = shipping_rates[0]["rate_id"]

        schedule_data = {
            "rate_id": selected_rate,  # Include the selected rate ID for scheduling
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
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

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
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        delivery = Delivery.objects.create(
            order=self.order_user,
            shipping_method=ShippingMethod.objects.create(name="USPS", price=10.0),
            tracking_number="123456789",
            shipping_label_url="http://example.com/label",
            status="pending"
        )

        response = self.client.get(reverse("check-delivery-status", args=(delivery.id,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)