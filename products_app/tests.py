from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import *


class BrandTestCase(APITestCase):
    
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username="test_admin_user", password="password")
        self.user = User.objects.create_user(username="test_user", password="password")
        self.brand = Brand.objects.create(name="Test", description="Test")
     
    def test_brand_list(self):
        response = self.client.get(reverse("brands"))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_brand_create_unathenticated(self):
        self.client.login(username="test_user", password="password")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        
        data = {
            "name": "Test",
            "description": "Test"
        }
        response = self.client.post(reverse("brand-create"), data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_brand_edit_unathenticated(self):
        self.client.login(username="test_user", password="password")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        
        data = {
            "name": "Test",
            "description": "Test"
        }
        
        response = self.client.put(reverse("brand-edit", args=(self.brand.id,)), data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_brand_delete_unathenticated(self):
        self.client.login(username="test_user", password="password")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        
        response = self.client.delete(reverse("brand-delete", args=(self.brand.id,)))
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_brand_create_admin(self):
        self.client.login(username="test_admin_user", password="password")
        self.token_admin = Token.objects.get(user__username=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {
            "name": "Test",
            "description": "Test"
        }
        response = self.client.post(reverse("brand-create"), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_brand_edit_put_admin(self):
        self.client.login(username="test_admin_user", password="password")
        self.token_admin = Token.objects.get(user__username=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)
        
        data = {
            "name": "Test - edited",
            "description": "Test"
        }

        response = self.client.put(reverse("brand-edit", args=(self.brand.id,)), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_brand_edit_patch_admin(self):
        self.client.login(username="test_admin_user", password="password")
        self.token_admin = Token.objects.get(user__username=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)
        
        data = {
            "name": "Test - edited",
            "description": "Test - edited"
        }

        response = self.client.put(reverse("brand-edit", args=(self.brand.id,)), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_brand_delete_admin(self):
        self.client.login(username="test_admin_user", password="password")
        self.token_admin = Token.objects.get(user__username=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.delete(reverse("brand-delete", args=(self.brand.id,)))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)