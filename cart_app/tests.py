from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from products_app.models import Brand, Category, Product

from .models import *


class CartTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create(username="test_user", password="password")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.brand = Brand.objects.create(name="Test brand", description="Test description")
        self.category = Category.objects.create(name="Test category", description="Test description")
        self.product = Product.objects.create(
                                            name="Test product",
                                            description="Test description",
                                            price=12.99,
                                            stock=654,
                                            category=self.category,
                                            brand=self.brand,
                                            )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity="12")
        
    def test_view_cart(self):
        response = self.client.get(reverse("cart"))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_add_cart_item(self):
        data = {
            "product_id": self.product.id,
            "quantity": "12"
        }
        response = self.client.post(reverse("cart-add"), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_edit_cart_item(self):
        data = {
            "cart": self.cart.id,
            "product": self.product.id,
            "quantity": "15"
        }

        response = self.client.put(reverse("cart_item-edit", args=(self.cart_item.id,)), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_cart_item(self):
        response = self.client.delete(reverse("cart_item-delete", args=(self.cart_item.id,)))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_clear_cart_items(self):
        response = self.client.delete(reverse("cart-clear"))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

