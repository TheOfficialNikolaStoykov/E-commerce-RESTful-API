from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from users_app.models import *


class UserTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="password")
        self.admin_user = User.objects.create_superuser(username="test_admin_user", password="password")


        self.user_profile = Profile.objects.create(
            user=self.user,
            first_name="Test",
            last_name="User",
            phone_number="+11234567890",
            address_line_1="Test Address 1",
            address_line_2="Test Address 2",
            city="Test City",
            postal_code=1999,
            state="Test State",
            country="Test Country"
        )

        self.admin_profile = Profile.objects.create(
            user=self.admin_user,
            first_name="Admin",
            last_name="User",
            phone_number="+11234567891",
            address_line_1="Admin Address 1",
            address_line_2="Admin Address 2",
            city="Admin City",
            postal_code=2000,
            state="Admin State",
            country="Admin Country"
        )

    def test_login(self):
        data = {
            "username": self.user.username,
            "password": "password"
        }
        
        response = self.client.post(reverse("login"), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_register(self):
        data = {
            "username": "new_user",
            "password": "new_password",
            "email": "new_user@example.com",
            "first_name": "New",
            "last_name": "User",
            "phone_number": "+11234567892",
            "address_line_1": "New Address 1",
            "address_line_2": "New Address 2",
            "city": "New City",
            "postal_code": 1234,
            "state": "New State",
            "country": "New Country"
        }
        
        response = self.client.post(reverse("register"), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logout(self):
        data = {
            "username": self.user.username,
            "password": "password"
        }

        response = self.client.post(reverse("login"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = Token.objects.get(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_profiles(self):
        self.client.login(username=self.admin_user.username, password="password")
        token_admin = Token.objects.get(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_admin.key)
 
        response = self.client.get(reverse("profiles"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_single_profile(self):
        self.client.login(username=self.admin_user.username, password="password")
        token_admin = Token.objects.get(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_admin.key)

        response = self.client.get(reverse("profile", args=(self.user_profile.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_single_profile_put(self):
        self.client.login(username=self.admin_user.username, password="password")
        token_admin = Token.objects.get(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_admin.key)

        data = {
            "username": self.user.username,
            "password": self.user.password,
            "email": "valid_email@example.com",
            "first_name": "ValidName",
            "last_name": "UpdatedLastName",
            "phone_number": "+14155552671",
            "address_line_1": "Updated Address 1",
            "address_line_2": "Updated Address 2",
            "city": "ValidCity",
            "state": "ValidState",
            "postal_code": 4321,
            "country": "ValidCntry"
        }

        response = self.client.put(reverse("profile-edit", args=(self.user_profile.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_single_profile_patch(self):
        self.client.login(username=self.admin_user.username, password="password")
        token_admin = Token.objects.get(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_admin.key)

        data = {
            "username": self.user.username,
            "password": self.user.password,
            "phone_number": "+14155552671",
            "first_name": "Test Name",
            "email": "example@example.com"
        }
        
        response = self.client.patch(reverse("profile-edit", args=(self.user_profile.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_single_profile(self):
        self.client.login(username=self.admin_user.username, password="password")
        token_admin = Token.objects.get(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token_admin.key)
        
        response = self.client.delete(reverse("profile-delete", args=(self.user_profile.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)