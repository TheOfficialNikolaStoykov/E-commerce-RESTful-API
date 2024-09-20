from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from cart_app.models import *
from orders_app.models import *
from payments_app.models import Payment
from products_app.models import *
from users_app.models import User


class UserTestCase(APITestCase):
    
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
        self.payment = Payment.objects.create(
            order=self.order_user,
            amount=self.order_user.total_price,
            status="pending",
            payment_method="stripe"
        )

     
    def test_process_payment(self):
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        
        response = self.client.post(reverse("process-payment", args=(self.order_user.id,)), {"payment_method": "stripe"})
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_payment_status(self):
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)
        
        response = self.client.get(reverse("get-payment-status", args=(self.payment.id,)))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)